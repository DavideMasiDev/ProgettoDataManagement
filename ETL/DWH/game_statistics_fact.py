from time import sleep
import pandas as pd
from utils.db_utils import select_rows, insert_rows, find_new_records, update_table

def load_records(dat_ini_val, dat_fin_val):

    # Gestione giochi mai inseriti in DWH

    query = ('select sg.steam_game_pk, rg.estimated_revenue, rg.average_forever, rg.total_positive as total_positive_reviews, rg.total_negative as total_negative_reviews, rg.estimated_wishlists '
             'from "STAGING".released_game rg '
             'join "DWH".steam_game sg on sg.steam_appid = rg.steam_appid')

    query_dwh = ('select steam_game_pk, estimated_revenue, average_forever, total_positive_reviews, total_negative_reviews, estimated_wishlists '
                 'from "DWH".game_statistics_fact')

    game_statistics = select_rows(query)
    game_statistics_dwh = select_rows(query_dwh)

    game_mai_inseriti = find_new_records(game_statistics, game_statistics_dwh, ['steam_game_pk'])

    game_mai_inseriti = game_mai_inseriti.values.tolist()
    for elem in game_mai_inseriti:
        elem.append(dat_ini_val)
        elem.append('9999-12-31')

    game_mai_inseriti = pd.DataFrame(game_mai_inseriti, columns = ['steam_game_pk', 'estimated_revenue', 'average_forever', 'total_positive_reviews', 'total_negative_reviews', 'estimated_wishlist', 'dat_ini_val', 'dat_fin_val'])

    insert_rows("DWH", "game_statistics_fact", game_mai_inseriti)


    # Gestione giochi già presenti in DWH

    game_da_aggiornare_query = ('with dwh as ( '
	'select sg.steam_appid, gsf.* '
	'from "DWH".game_statistics_fact gsf '
	'join "DWH".steam_game sg on (sg.steam_game_pk = gsf.steam_game_pk)) '
    'select dwh.steam_game_pk, rg.estimated_revenue, rg.average_forever, rg.total_positive as total_positive_reviews, rg.total_negative as total_negative_reviews, rg.estimated_wishlists '
    'from "STAGING".released_game rg '
    'join dwh on (dwh.steam_appid = rg.steam_appid) '
    'where ( rg.estimated_revenue::numeric != dwh.estimated_revenue '
	'or rg.average_forever::numeric  != dwh.average_forever '
	'or rg.total_positive::numeric != dwh.total_positive_reviews '
	'or rg.total_negative::numeric != dwh.total_negative_reviews '
	'or rg.estimated_wishlists::numeric != dwh.estimated_wishlists)')

    game_da_aggiornare = select_rows(game_da_aggiornare_query)
    game_da_aggiornare = game_da_aggiornare.values.tolist()

    da_inserire = []
    for elem in game_da_aggiornare:

        print(elem, flush=True)

        query_max_record = ('select * '
                            'from "DWH".game_statistics_fact gsf '
                            + "where dat_fin_val = '9999-12-31' and steam_game_pk = " + str(elem[0]))

        max_record = select_rows(query_max_record).values.tolist()[0]

        print(max_record, flush=True)

        update_query = ('update "DWH".game_statistics_fact set dat_fin_val=' + "'" + dat_fin_val + "'" +
                        ' where game_statistics_fact_pk = ' + str(max_record[0]))
        update_table(update_query)

        elem.append(dat_ini_val)
        elem.append('9999-12-31')
        da_inserire.append(elem)

    da_inserire = pd.DataFrame(da_inserire, columns = ['steam_game_pk', 'estimated_revenue', 'average_forever', 'total_positive_reviews', 'total_negative_reviews', 'estimated_wishlists', 'dat_ini_val', 'dat_fin_val'])

    insert_rows("DWH", "game_statistics_fact", da_inserire)

    return None
