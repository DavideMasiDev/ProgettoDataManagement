from utils.db_utils import select_rows, insert_rows


def load_records(data_inizio_periodo, data_fine_periodo):
    if data_inizio_periodo is not None and data_fine_periodo is not None:
        query = ("select df.*"
                " from \"DWH\".deal_fact df"
                " join \"DWH\".date dt on dt.date_pk = df.deal_date_pk"
               f" where dt.full_date::date >= \'{data_inizio_periodo}\'"
               f" and dt.full_date::date <= \'{data_fine_periodo}\'")

        selected_rows = select_rows(query)

        insert_rows('DATAMART', 'deal_fact', selected_rows)

    else:
        print('\n[ERROR] data_inizio_periodo and data_fine_periodo can not be None')

    return None