import json
import os
import pandas as pd
from tqdm import tqdm
from ETL.utils.db_utils import insert_rows

INPUT_FOLDER = "raw_sources/aug-25-raw-data/raw"
TABLE_NAME = "raw_data"
SCHEMA_NAME = "STAGING"

def load_records(input_path):
    records = []
    files = [f for f in os.listdir(input_path) if f.endswith(".json")]
    for filename in tqdm(files, desc="Processing JSON files", unit="file"):
        filepath = os.path.join(input_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for appid, game in data.items():
            try:
                if game.get("type") != "dlc" and game.get("type") != "game":
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

    insert_rows(SCHEMA_NAME, TABLE_NAME, records)

    return None