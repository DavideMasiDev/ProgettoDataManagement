import os
import json
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

# cartella con i file json raw
INPUT_FOLDER = "raw_sources/aug-25-raw-data/raw"
OUTPUT_FILE = "clean_sources/raw_data.csv"


# def clean_html(raw_html: str) -> str:
#     """Rimuove tag HTML e restituisce solo testo pulito"""
#     if not raw_html:
#         return ""
#     return BeautifulSoup(raw_html, "html.parser").get_text(separator=" ").strip()


records = []
files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".json")]

for filename in tqdm(files, desc="Processing JSON files", unit="file"):
    filepath = os.path.join(INPUT_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for appid, game in data.items():
        try:
            gtype = game.get("type")
            if gtype not in ("game", "dlc"):  # 🔹 filtro: solo game o dlc
                continue

            record = {
                "steam_appid": game.get("steam_appid"),
                "type": game.get("type"),
                "name": game.get("name"),
            }

            # fullgame (solo se DLC)
            if game.get("type") == "dlc":
                record["fullgame"] = (
                    game.get("fullgame", {}).get("appid")
                    if isinstance(game.get("fullgame"), dict)
                    else None
                )
            else:
                record["fullgame"] = None

            # pc_requirements come JSON pulito da HTML
            # pc_req = game.get("pc_requirements", {})
            # if isinstance(pc_req, dict):
            #     record["pc_requirements"] = json.dumps({
            #         "minimum": clean_html(pc_req.get("minimum", "")),
            #         "recommended": clean_html(pc_req.get("recommended", ""))
            #     }, ensure_ascii=False)
            # else:
            #     record["pc_requirements"] = json.dumps({
            #         "minimum": "",
            #         "recommended": ""
            #     })

            records.append(record)

        except Exception as e:
            print(f"Errore parsing appid {appid}: {e}")

# converto in DataFrame e salvo CSV
df = pd.DataFrame(records, columns=[
    "steam_appid",
    "type",
    "name",
    "fullgame",
    # "pc_requirements"
])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\n✅ Conversione completata: {len(records)} record totali salvati in {OUTPUT_FILE}")
