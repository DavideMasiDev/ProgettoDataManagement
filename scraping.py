import requests
import csv
import time
from datetime import datetime, timezone

API_KEY = "cae48f2d7db01e9403cce10a083597c6e3b49696"
COUNTRY = "IT"
REGION = "eu"
SHOP = 61
TIMEOUT = 1

# 1. Ottieni plain da IsThereAnyDeal via search
def get_plain_from_name(name):
    url = "https://api.isthereanydeal.com/games/search/v1"
    params = {
        "key": API_KEY,
        "title": name
    }
    r = requests.get(url, params=params)
    results = r.json()
    if results and results[0] and results[0]["id"]:
        return results[0]["id"]
    else:
        return None

# 2. Ottieni storico prezzi
def get_price_history(plain, release_date):
    url = "https://api.isthereanydeal.com/games/history/v2"
    params = {
        "key": API_KEY,
        "id": plain,
        "country": COUNTRY,
        "shops": [SHOP],
        "since": release_date
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data

# 3. Salva in CSV
def save_to_csv(price_data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "price",
            "deal",
            "regular_price",
            "currency"
        ])
        for entry in price_data:
            writer.writerow([
                entry["timestamp"],
                entry["deal"]["price"]["amount"],
                entry["deal"]["cut"],
                entry["deal"]["regular"]["amount"],
                entry["deal"]["price"]["currency"]
            ])
    print(f"[✓] Dati salvati in {filename}")

# 4. Ottieni data rilascio
def get_release_date(plain):
    url = "https://api.isthereanydeal.com/games/info/v2"
    params = {
        "key": API_KEY,
        "id": plain
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["releaseDate"]

# === ESECUZIONE ===

with open('giochi.txt', 'r', encoding='utf-8') as file:
    names = [riga.strip() for riga in file]

for name in names:
    print(f"[i] Cerco 'plain' per: {name}")
    plain = get_plain_from_name(name)
    if not plain:
        print("[!] Nessun 'plain' trovato per questo gioco.")
    else:
        print(f"[i] Plain corrispondente: {plain}")
        release_date = get_release_date(plain)
        if not release_date:
            print("[!] Nessuna data di rilascio trovata")
        else:
            release_date = datetime.strptime(release_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).isoformat()
            print(f"[i] Data di rilascio: {release_date}")
            data = get_price_history(plain, release_date)
            save_to_csv(data, f"./storici/storico_prezzi_{name}.csv")
    time.sleep(TIMEOUT)

