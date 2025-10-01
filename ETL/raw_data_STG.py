import json
import os
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm

# Config Postgres
DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steamdb"

INPUT_FOLDER = "raw_sources/aug-25-raw-data/raw"
OUTPUT_FILE = "clean_sources/raw_data.csv"
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
    return records

def main():
    # 1) Load and normalize
    records = load_records(INPUT_FOLDER)
    df = pd.DataFrame(records, columns=["steam_appid", "type", "name", "fullgame"])
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