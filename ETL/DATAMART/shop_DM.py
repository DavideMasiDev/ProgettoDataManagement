from utils.db_utils import insert_rows, select_rows

def load_records():

    query_shop_dwh = 'select shop_pk, shop_name from "DWH".shop'
    query_shop_dwh = select_rows(query_shop_dwh)

    insert_rows("DATAMART", "shop", query_shop_dwh)

    return None