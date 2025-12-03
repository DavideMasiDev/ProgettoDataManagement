import json
import os
import pandas as pd
from tqdm import tqdm
from utils.db_utils import insert_rows, truncate_table, update_table, select_rows

TABLE_NAME = "raw_data"
SCHEMA_NAME = "STAGING"

def load_records(input_path):
    records = []
    games = []

    files = [f for f in os.listdir(input_path) if f.endswith(".json")]
    for filename in tqdm(files, desc="Processing JSON files", unit="file"):
        filepath = os.path.join(input_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)


        for appid, game in data.items():
            try:
                if (game.get("type") != "dlc" and game.get("type") != "game") or game.get('name') == '':
                    continue
                else:
                    record = {
                        "steam_appid": int(appid),
                        "type": game.get("type"),
                        "name": game.get("name")
                    }

                    if game.get("type") == "dlc":
                        record["fullgame"] = (
                            int(game.get("fullgame", {}).get("appid"))
                            if isinstance(game.get("fullgame"), dict)
                            else None
                        )
                    else:
                        record["fullgame"] = None

                    records.append(record)

            except Exception as e:
                # log minimo: continua con gli altri record
                print(f"Warning parsing appid {appid}: {e}")

    records = pd.DataFrame(records, columns=["steam_appid", "type", "name", "fullgame"])

    print(f"Dropping old records from {TABLE_NAME} table")
    truncate_table(SCHEMA_NAME, TABLE_NAME)
    print(f"Inserting {len(records)} records into {TABLE_NAME} table")
    insert_rows(SCHEMA_NAME, TABLE_NAME, records)

    query = ('select distinct on (name)'
             ' steam_appid,'
             ' name,'
             ' type,'
             ' fullgame'
             ' from "STAGING".raw_data'
             ' order by name, steam_appid asc;')
    records = select_rows(query)

    print(f"Dropping duplicated records from {TABLE_NAME} table")
    truncate_table(SCHEMA_NAME, TABLE_NAME)
    print(f"Inserting {len(records)} non-duplicates records into {TABLE_NAME} table")
    insert_rows(SCHEMA_NAME, TABLE_NAME, records)

    games_list = records.values.tolist()
    for game in games_list:
        games.append({"steam_appid": game[0], "name": game[1]})

    return games