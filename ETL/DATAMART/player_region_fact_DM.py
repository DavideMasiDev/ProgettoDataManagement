from utils.db_utils import select_rows, insert_rows

def load_records(data_inizio_periodo, data_fine_periodo):
    if data_inizio_periodo is not None and data_fine_periodo is not None:
        query = ("select prf.steam_game_pk, count(prf.player_pk) AS player_counter, p.region, p.country_code, prf.dat_ini_val, prf.dat_fin_val"
                 " from \"DWH\".player_region_fact prf"
                 " join \"DWH\".player p ON prf.player_pk = p.player_pk"
                 f" where prf.dat_fin_val::date >= \'{data_inizio_periodo}\'"
                 f" and prf.dat_ini_val::date <= \'{data_fine_periodo}\'"
                 " group by prf.steam_game_pk, p.region, p.country_code, prf.dat_ini_val, prf.dat_fin_val")

        selected_rows = select_rows(query)

        insert_rows('DATAMART', 'player_region_fact', selected_rows)

    else:
        print('\n[ERROR] data_inizio_periodo and data_fine_periodo can not be None')

    return None