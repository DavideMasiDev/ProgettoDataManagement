from utils.db_utils import insert_rows, select_rows, truncate_table

def load_records():

    query_currency_dwh = 'select currency_pk, currency_name, currency_code from "DWH".currency'
    query_currency_dwh = select_rows(query_currency_dwh)

    insert_rows("DATAMART", "currency", query_currency_dwh)

    return None