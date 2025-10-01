import os
import json
import pandas as pd
from sqlalchemy import create_engine

# Config Postgres
DB_URI = "postgresql+psycopg2://myuser:mypassword@localhost:5432/steamdb"

INPUT_FILE = "raw_sources/aug-25-game-player-regions.json"
OUTPUT_FILE = "clean_sources/aug-25-game-player-regions.csv"
TABLE_NAME = "players"

# === 1. Carico JSON e normalizzo in records ===
records = []
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for appid, players in data.items():
    for player in players:
        records.append({
            "steam_appid": int(appid),
            "player_steamid": int(player.get("player_steamid", 0)),
            "region": player.get("region", ""),
            "country_code": player.get("countryCode", "")
        })

# === 2. Creo DataFrame ===
df = pd.DataFrame(records, columns=["steam_appid", "player_steamid", "region", "country_code"])

# === 3. Esporto CSV ===
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"✅ Creato CSV: {OUTPUT_FILE} ({len(df)} record)")

# === 4. Carico in Postgres ===
engine = create_engine(DB_URI)

# Crea la tabella se non esiste
with engine.begin() as conn:
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        steam_appid BIGINT,
        player_steamid BIGINT,
        region TEXT,
        country_code TEXT
    );
    """)

# Carica i dati
df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)
print(f"✅ Inseriti {len(df)} record in Postgres (tabella {TABLE_NAME})")
