from utils.db_utils import insert_rows, select_rows

def load_records():

    query_player_dwh = 'select player_pk, player_steamid, region, country_code from "DWH".player'
    query_player_dwh = select_rows(query_player_dwh)

    insert_rows("DATAMART", "player", query_player_dwh)

    return None