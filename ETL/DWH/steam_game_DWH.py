from utils.db_utils import select_rows, insert_rows, find_new_records


def load_records():

    query_staging = ('select rd.steam_appid, rd.name as game_name, rd."type", rd.fullgame, dt.date_pk as release_date_pk '
             'from "STAGING".raw_data rd '
             'join "STAGING".released_game rg on rd.steam_appid = rg.steam_appid '
             'join "DWH".date dt on dt.full_date = rg.release_date')

    query_dwh = ('select sg.steam_appid, sg.game_name, sg."type", sg.fullgame, sg.release_date_pk '
                 'from "DWH".steam_game sg')

    staging_rows = select_rows(query_staging)
    dwh_rows = select_rows(query_dwh)

    new_rows = find_new_records(staging_rows, dwh_rows, key_column='steam_appid')

    insert_rows("DWH", "steam_game", new_rows)

    return None

def main():
    load_records()
if __name__ == '__main__':
    main()