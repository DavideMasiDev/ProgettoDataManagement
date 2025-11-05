from utils.db_utils import insert_rows, select_rows, truncate_table

def load_records():

    query_steam_game_dwh = 'select steam_appid, game_name, type, fullgame, release_date_pk from "DWH".steam_game'
    query_steam_game_dwh = select_rows(query_steam_game_dwh)

    truncate_table("DATAMART", "steam_game")
    insert_rows("DATAMART", "steam_game", query_steam_game_dwh)

    return None