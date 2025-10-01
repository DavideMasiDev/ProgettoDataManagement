import os
import json
import pandas as pd
from tqdm import tqdm  # opzionale, per progress bar

INPUT_FILE = "raw_sources/aug-25-game-player-regions.json"
OUTPUT_FILE = "clean_sources/aug-25-game-player-regions.csv"

records = []

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for appid, players in tqdm(data.items(), desc="Processing appids", unit="appid"):
    for player in players:
        try:
            records.append({
                "steam_appid": int(appid),
                "player_steamid": int(player.get("player_steamid", 0)),
                "region": player.get("region", ""),
                "country_code": player.get("countryCode", "")
            })
        except Exception as e:
            print(f"Errore parsing appid {appid}: {e}")

# converto in DataFrame e salvo CSV
df = pd.DataFrame(records, columns=["steam_appid", "player_steamid", "region", "country_code"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\n✅ Conversione completata: {len(records)} record totali salvati in {OUTPUT_FILE}")
