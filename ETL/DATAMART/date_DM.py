from utils.db_utils import insert_rows, select_rows, truncate_table

def load_records():

    query_date_dwh = 'select date_pk, full_date, year, month, day, day_of_week, day_name, month_name from "DWH".date'
    query_date_dwh = select_rows(query_date_dwh)

    insert_rows("DATAMART", "date", query_date_dwh)

    return None