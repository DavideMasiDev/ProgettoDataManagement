import json
import pandas as pd
from tqdm import tqdm
from utils.db_utils import insert_rows

TABLE_NAME = "game_player_region"
SCHEMA_NAME = "STAGING"

def load_records(input_path):
    records = []
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for appid, players in tqdm(data.items(), desc="Parsing appids", unit="appid"):
        for p in players:
            try:
                records.append({
                    "steam_appid": int(appid),
                    "player_steamid": int(p.get("player_steamid", 0)),
                    "region": p.get("region", ""),
                    "country_code": p.get("countryCode", "")
                })
            except Exception as e:
                # log minimo: continua con gli altri record
                print(f"Warning parsing appid {appid}: {e}")

    records = pd.DataFrame(records, columns=["steam_appid", "player_steamid", "region", "country_code"])

    insert_rows(SCHEMA_NAME, TABLE_NAME, records)

    return None
