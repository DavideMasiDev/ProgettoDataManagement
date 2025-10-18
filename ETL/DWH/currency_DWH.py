from utils.db_utils import select_rows, insert_rows, find_new_records

def load_records():

    query = 'select distinct currency as currency_code from "STAGING".price_history'
    currencies = select_rows(query)

    # Recuperiamo i record già inseriti in DWH in modo da non creare duplicati nella tabella,
    # essendo quest'ultima solamente una tipologica.
    # Verranno inseriti solamente currency che non erano già presenti.

    query = 'select currency_code from "DWH".currency'
    dwh_currencies = select_rows(query)

    currencies = find_new_records(currencies, dwh_currencies, ['currency_code'])

    currency_name = {"EUR": "Euro", "USD": "Dollaro Statunitense", "GBP": "Sterlina Britannica"}
    currencies["currency_name"] = currencies["currency_code"].map(currency_name)

    insert_rows("DWH", "currency", currencies)

    return None