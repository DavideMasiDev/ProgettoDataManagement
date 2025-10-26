from utils.db_utils import select_rows, insert_rows

def load_records(dat_ini_val, dat_fin_val):

    query = ('select sg.steam_game_pk, rg.estimated_revenue, rg.average_forever, rg.total_positive as total_positive_reviews, rg.total_negative as total_negative_reviews, rg.estimated_wishlists '
             'from "STAGING".released_game rg '
             'join "DWH".steam_game sg on sg.steam_appid = rg.steam_appid')

    game_statistics = select_rows(query)

    game_statistics['dat_ini_val'] = dat_ini_val
    game_statistics['dat_fin_val'] = dat_fin_val

    insert_rows("DWH", "game_statistics_fact", game_statistics)

    return None