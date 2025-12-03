import threading
import requests
import time
import sys
import pandas as pd
from datetime import datetime, timezone
from utils.db_utils import insert_rows, truncate_table, select_rows

SCHEMA_NAME = "STAGING"
TABLE_NAME = "price_history"
COUNTRY = "IT"
REGION = "eu"
SHOP = 61
TIMEOUT = 0.5
BATCH_SIZE = 1000

def get_plain_from_name(name, api_key):
    url = "https://api.isthereanydeal.com/games/search/v1"
    params = {
        "key": api_key,
        "title": name
    }
    r = requests.get(url, params=params)
    if r.ok:
        try:
            results = r.json()
            if results and results[0] and results[0]["id"]:
                return results[0]["id"]
            else:
                return None
        except requests.exceptions.JSONDecodeError:
            print(f'\n[ERROR] Could not parse plain of {name} as JSON.')
            print(f'{r.text[:200]}')
            return None
    else:
        print(f'\n[ERROR] Could not get plain for {name}.')
        print(f'\n{r.text[:200]}')
        return None

def get_price_history(plain, release_date, api_key):
    url = "https://api.isthereanydeal.com/games/history/v2"
    params = {
        "key": api_key,
        "id": plain,
        "country": COUNTRY,
        "since": release_date
    }
    r = requests.get(url, params=params)
    if r.ok:
        try:
            data = r.json()
            if data:
                return data
            else:
                return None
        except requests.exceptions.JSONDecodeError:
            print(f'\n[ERROR] Could not parse as JSON the price history for plain code: {plain}.')
            print(f'\n{r.text[:200]}')
            return None
    else:
        print(f'\n[ERROR] Could not get price history for plain code: {plain}.')
        print(f'\n{r.text[:200]}')
        return None

def save_batch_to_db(batch, schema_name, table_name):
    df = pd.DataFrame(batch, columns=["steam_appid", "name", "timestamp", "price", "deal", "regular_price", "currency", "shop"])
    insert_rows(schema_name, table_name, df)

def format_records(data, steam_appid, game_name):
    if not data or len(data) == 0:
        return None

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

    return records

def get_release_date(plain, api_key):
    url = "https://api.isthereanydeal.com/games/info/v2"
    params = {
        "key": api_key,
        "id": plain
    }
    r = requests.get(url, params=params)
    if r.ok:
        try:
            data = r.json()
            if data:
                data = r.json()
                return data["releaseDate"]
            else:
                return None
        except requests.exceptions.JSONDecodeError:
            print(f'\n[ERROR] Could not parse as JSON the release date for plain code: {plain}.')
            print(f'\n{r.text[:200]}')
            return None
    else:
        print(f'\n[ERROR] Could not get release date for plain code: {plain}.')
        print(f'\n{r.text[:200]}')
        return None

def get_last_dates_for_game():
    query = ("select steam_appid, max(d.full_date)::date as timestamp"
            " from \"DWH\".deal_fact df"
            " join \"DWH\".steam_game sg on sg.steam_game_pk = df.steam_game_pk"
            " join \"DWH\".date d on d.date_pk = df.deal_date_pk"
            " group by steam_appid")

    last_dates_for_game = select_rows(query)

    if last_dates_for_game is not None and len(last_dates_for_game) > 0:
        return last_dates_for_game.values.tolist()
    else:
        return []


def get_last_date(steam_appid, dates_list: list):
    for date in dates_list:
        # date[0] contains the steam_appid, date[1] contains the timestamp
        if str(date[0]) == steam_appid:
            return date[1].strftime('%Y-%m-%d')

    return None

def format_time(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def print_loading_bar(iteration, total, start_time, bar_len=30):

    percent = int((iteration / total) * 100)
    fill = int(bar_len * iteration // total)
    loading_bar = '█' * fill + '-' * (bar_len - fill)

    time_elapsed = time.time() - start_time
    if iteration > 0:
        time_fot_item = time_elapsed / iteration
        time_remaining  = time_fot_item * (total - iteration)
    else:
        time_remaining  = 0

    time_elapsed_fmt = format_time(time_elapsed)
    time_remaining_fmt = format_time(time_remaining)

    output = (
        f"\r|{loading_bar}| {percent:3d}% "
        f"({iteration}/{total}) "
        f"⏱️ {time_elapsed_fmt} elapsed, ⏳ {time_remaining_fmt} left"
    )
    sys.stdout.write(output)
    sys.stdout.flush()

    if iteration == total:
        print()


def load_records(games, primo_caricamento, api_key):

    print('Avvio dello scraper per l\'acquisizione dello storico prezzi di ogni gioco.\n')

    if games is None:
        games = []
    index = 0
    totale_giochi = len(games)
    start_time = time.time()

    current_batch = []
    threads = []

    truncate_table(SCHEMA_NAME, TABLE_NAME)

    last_dates_for_game = []

    if not primo_caricamento:
        last_dates_for_game = get_last_dates_for_game()

    for game in games:
        plain = get_plain_from_name(game["name"], api_key)

        if plain:
            if primo_caricamento:
                # start_date = get_release_date(plain, api_key)
                start_date = '2024-01-01'
            else:
                start_date = get_last_date(game["steam_appid"], last_dates_for_game)

            if start_date is not None:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).isoformat()
                data = get_price_history(plain, start_date, api_key)
                if data:
                    new_records = format_records(data, game["steam_appid"], game["name"])
                    if new_records:
                        current_batch.extend(new_records)


        if len(current_batch) >= BATCH_SIZE:
            to_save = current_batch.copy()

            t = threading.Thread(
                target=save_batch_to_db,
                args=(to_save, SCHEMA_NAME, TABLE_NAME)
            )
            t.start()
            threads.append(t)
            current_batch.clear()

            active_threads = [t for t in threads if t.is_alive()]
            threads = active_threads

        print_loading_bar(index, totale_giochi, start_time)
        index += 1
        time.sleep(TIMEOUT)

    if current_batch:
        t = threading.Thread(
            target=save_batch_to_db,
            args=(current_batch, SCHEMA_NAME, TABLE_NAME)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()