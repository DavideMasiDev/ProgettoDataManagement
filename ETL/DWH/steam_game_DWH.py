from utils.db_utils import select_rows, insert_rows

def load_records():

    query = ('select rd.steam_appid, rd.name as game_name, rd."type", rd.fullgame, dt.date_pk as release_date_pk '
             'from "STAGING".raw_data rd '
             'join "STAGING".released_game rg on rd.steam_appid = rg.steam_appid '
             'join "DWH".date dt on dt.full_date = rg.release_date')

    steam_game_rows = select_rows(query)

    insert_rows("DWH", "steam_game", steam_game_rows)

    return None

def main():
    load_records()

if __name__ == '__main__':
    main()
