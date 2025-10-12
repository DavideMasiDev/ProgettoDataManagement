import requests
import csv
import time
import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timezone

# TODO: add your key here
API_KEY = "cae48f2d7db01e9403cce10a083597c6e3b49696"
DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steamdb"
SCHEMA_NAME = "STAGING"
TABLE_NAME = "price_history"
COUNTRY = "IT"
REGION = "eu"
SHOP = 61
TIMEOUT = 0.5
DEBUG = False

# 1. Ottieni plain da IsThereAnyDeal via search
def get_plain_from_name(name, api_key):
    url = "https://api.isthereanydeal.com/games/search/v1"
    params = {
        "key": api_key,
        "title": name
    }
    r = requests.get(url, params=params)
    results = r.json()
    if results and results[0] and results[0]["id"]:
        return results[0]["id"]
    else:
        return None

# 2. Ottieni storico prezzi
def get_price_history(plain, release_date, api_key):
    url = "https://api.isthereanydeal.com/games/history/v2"
    params = {
        "key": api_key,
        "id": plain,
        "country": COUNTRY,
        "since": release_date
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data

# 3. Inizializza connessione a DB
def init_db_connection(db_uri):
    # Connessione DB
    engine = create_engine(db_uri)
    return engine.connect()

# 4. Salva a DB
def save_to_db(data, steam_appid, game_name, conn, schema_name, table_name):
    """
    Inserisce i dati di prezzo nel database (schema STAGING.price_history)
    """
    if not data or len(data) == 0:
        if DEBUG: print(f"[!] Nessun dato di prezzo per {game_name}")
        return

    # Creo il record das caricare a DB
    records = []
    for deal in data:
        records.append({
            "steam_appid": steam_appid,
            "name": game_name,
            "timestamp": deal["timestamp"],
            "price": deal["deal"]["price"]["amount"],
            "deal": deal["deal"]["cut"],
            "regular_price": deal["deal"]["regular"]["amount"],
            "currency": deal["deal"]["price"]["currency"],
            "shop": deal["shop"]["name"]
        })

    df = pd.DataFrame(records, columns=["steam_appid", "name", "timestamp", "price", "deal", "regular_price", "currency", "shop"])

    # Inserisci nel DB
    try:
        df.to_sql(
            table_name,
            con=conn,
            schema=schema_name,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000
        )
        if DEBUG: print(f"[+] Inseriti {len(df)} record per {game_name}")
    except Exception as e:
        print(f"[!] Errore durante l'inserimento di {game_name}: {e}")

# 5. Ottieni data rilascio
def get_release_date(plain, api_key):
    url = "https://api.isthereanydeal.com/games/info/v2"
    params = {
        "key": api_key,
        "id": plain
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data["releaseDate"]

# 6. Stampa percentuale progresso
def barra_di_caricamento(iterazione, totale, start_time, lunghezza=30):
    # Calcolo percentuale e barra
    percentuale = int((iterazione / totale) * 100)
    riempimento = int(lunghezza * iterazione // totale)
    barra = '█' * riempimento + '-' * (lunghezza - riempimento)

    # Calcolo tempo trascorso e stimato
    tempo_trascorso = time.time() - start_time
    if iterazione > 0:
        tempo_per_item = tempo_trascorso / iterazione
        tempo_rimanente = tempo_per_item * (totale - iterazione)
    else:
        tempo_rimanente = 0

    # Formatta il tempo in hh:mm:ss
    def format_time(seconds):
        h, rem = divmod(int(seconds), 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    tempo_trascorso_fmt = format_time(tempo_trascorso)
    tempo_rimanente_fmt = format_time(tempo_rimanente)

    # Output su una singola riga
    output = (
        f"\r|{barra}| {percentuale:3d}% "
        f"({iterazione}/{totale}) "
        f"⏱️ {tempo_trascorso_fmt} elapsed, ⏳ {tempo_rimanente_fmt} left"
    )
    sys.stdout.write(output)
    sys.stdout.flush()

    # A capo al completamento
    if iterazione == totale or DEBUG:
        print()

# === ESECUZIONE ===
def load_price_history_scraper(db_uri, schema_name, table_name, api_key, games=None):
    if games is None:
        games = []

    conn = init_db_connection(db_uri)
    index = 0
    totale_giochi = len(games)
    start_time = time.time()
    for game in games:

        if DEBUG: print(f"[i] Cerco 'plain' per: {game["name"]}")
        plain = get_plain_from_name(game["name"], api_key)
        if not plain:
            if DEBUG: print("[!] Nessun 'plain' trovato per questo gioco.")
        else:
            if DEBUG: print(f"[i] Plain corrispondente: {plain}")
            release_date = get_release_date(plain, api_key)
            if not release_date:
                if DEBUG: print("[!] Nessuna data di rilascio trovata")
            else:
                release_date = datetime.strptime(release_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).isoformat()
                if DEBUG: print(f"[i] Data di rilascio: {release_date}")
                data = get_price_history(plain, release_date, api_key)
                save_to_db(data, game["steam_appid"], game["name"], conn, schema_name, table_name)
        barra_di_caricamento(index, totale_giochi, start_time)
        index += 1
        time.sleep(TIMEOUT)

def main():
    load_price_history_scraper(DB_URI, SCHEMA_NAME, TABLE_NAME, API_KEY)

if __name__ == "__main__":
    main()