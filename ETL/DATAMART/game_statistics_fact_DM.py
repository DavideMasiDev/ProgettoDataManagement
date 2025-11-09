from utils.db_utils import select_rows, insert_rows


def load_records(data_inizio_periodo, data_fine_periodo):
    if data_inizio_periodo is not None and data_fine_periodo is not None:
        query = ("select gsf.*"
                " from \"DWH\".game_statistics_fact gsf"
               f" where gsf.dat_fin_val::date >= \'{data_inizio_periodo}\'"
               f" and gsf.dat_ini_val::date <= \'{data_fine_periodo}\'")

        selected_rows = select_rows(query)

        insert_rows('DATAMART', 'game_statistics_fact', selected_rows)

    else:
        print('\n[ERROR] data_inizio_periodo and data_fine_periodo can not be None')

    return None