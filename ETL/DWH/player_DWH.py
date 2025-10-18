from utils.db_utils import select_rows, insert_rows, find_new_records

def load_records():

    query = 'select distinct player_steamid, region, country_code from "STAGING".game_player_region'
    players = select_rows(query)

    # Recuperiamo i record già inseriti in DWH in modo da non creare duplicati nella tabella,
    # essendo quest'ultima solamente una tipologica.
    # Verranno inseriti solamente currency che non erano già presenti.

    query = 'select player_steamid, region, country_code from "DWH".player'
    dwh_players = select_rows(query)

    players = find_new_records(players, dwh_players, ['player_steamid', 'region', 'country_code'])

    insert_rows("DWH", "player", players)

    return None
