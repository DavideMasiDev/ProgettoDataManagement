from utils.db_utils import select_rows, insert_rows, find_new_records

def load_records():

    query = 'select distinct shop as shop_name from "STAGING".price_history'
    shops = select_rows(query)

    # Recuperiamo i record già inseriti in DWH in modo da non creare duplicati nella tabella,
    # essendo quest'ultima solamente una tipologica.
    # Verranno inseriti solamente currency che non erano già presenti.

    query = 'select shop_name from "DWH".shop'
    dwh_shops = select_rows(query)

    shops = find_new_records(shops, dwh_shops, ['shop_name'])

    insert_rows("DWH", "shop", shops)

    return None
