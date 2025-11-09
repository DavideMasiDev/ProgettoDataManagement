from utils.db_utils import insert_rows, select_rows, truncate_table

def load_records():

    query_genre_dwh = 'select genre_pk, genre_name from "DWH".genre'
    query_genre_dwh = select_rows(query_genre_dwh)

    insert_rows("DATAMART", "genre", query_genre_dwh)

    return None