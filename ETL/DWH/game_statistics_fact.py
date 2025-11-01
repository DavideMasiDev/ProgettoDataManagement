import pandas as pd
from utils.db_utils import select_rows, insert_rows, find_new_records, update_table

def chiudi_ultimo_record(key: list):
    return None

def load_records(dat_ini_val, dat_fin_val):

    query = ('select sg.steam_game_pk, rg.estimated_revenue, rg.average_forever, rg.total_positive as total_positive_reviews, rg.total_negative as total_negative_reviews, rg.estimated_wishlists '
             'from "STAGING".released_game rg '
             'join "DWH".steam_game sg on sg.steam_appid = rg.steam_appid')

    query_dwh = 'select * from "DWH".game_statistics_fact'

    game_statistics = select_rows(query)
    game_statistics_list = game_statistics.values.tolist()
    game_statistics_dwh = select_rows(query_dwh)

    # Gestione giochi mai inseriti in DWH

    game_mai_inseriti = find_new_records(game_statistics, game_statistics_dwh, ['steam_game_pk'])
    game_da_aggiornare = find_new_records(game_statistics, game_mai_inseriti, ['steam_game_pk'])

    game_mai_inseriti = game_mai_inseriti.values.tolist()
    for elem in game_mai_inseriti:
        elem.append(dat_ini_val)
        elem.append('9999-12-31')

    game_mai_inseriti = pd.DataFrame(game_mai_inseriti, columns = ['steam_game_pk', 'estimated_revenue', 'average_forever', 'total_positive_reviews', 'total_negative_reviews', 'estimated_wishlists', 'dat_ini_val', 'dat_fin_val'])

    insert_rows("DWH", "game_statistics_fact", game_mai_inseriti)

    # Gestione giochi già presenti in DWH

    game_da_aggiornare = game_da_aggiornare.values.tolist()
    da_inserire = []
    for elem in game_da_aggiornare:

        query_max_record = ('select * '
                            'from "DWH".game_statistics_fact gsf '
                            "where dat_fin_val = '9999-12-31' and steam_game_pk = " + elem[0])

        max_record = select_rows(query_max_record).values.tolist()[0]

        if(max_record[1] != elem[0]
           or max_record[2] != elem[1]
           or max_record[3] != elem[2]
           or max_record[4] != elem[3]
           or max_record[5] != elem[4]
           or max_record[6] != elem[5]):

            update_query = ('update "DWH".game_statistics_fact set dat_fin_val=' + dat_fin_val +
                            ' where game_statistics_fact_pk = ' + elem[0])
            update_table(update_query)

            elem.append(dat_ini_val)
            elem.append('9999-12-31')
            da_inserire.append(elem)

    da_inserire = pd.DataFrame(da_inserire, columns = ['steam_game_pk', 'estimated_revenue', 'average_forever', 'total_positive_reviews', 'total_negative_reviews', 'estimated_wishlists', 'dat_ini_val', 'dat_fin_val'])

    insert_rows("DWH", "game_statistics_fact", da_inserire)

    return None

def main():
    load_records()

if __name__ == "__main__":
    main()