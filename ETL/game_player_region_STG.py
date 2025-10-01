import json
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm

# Config Postgres
DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steamdb"

INPUT_FILE = "raw_sources/aug-25-game-player-regions.json"
OUTPUT_FILE = "clean_sources/aug-25-game-player-regions.csv"
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
    return records

def main():
    # 1) Load and normalize
    records = load_records(INPUT_FILE)
    df = pd.DataFrame(records, columns=["steam_appid", "player_steamid", "region", "country_code"])
    print(f"* Records parsed: {len(df)}")

    # 2) Save CSV (staging)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"* CSV creato: {OUTPUT_FILE}")

    # 3) Connect to Postgres
    engine = create_engine(DB_URI)

    # 4) Carico dati in Postgres
    df.to_sql(TABLE_NAME, engine, schema=SCHEMA_NAME, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"* Inseriti {len(df)} record nella tabella '{TABLE_NAME}'")


if __name__ == "__main__":
    main()