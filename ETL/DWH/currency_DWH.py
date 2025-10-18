from utils.db_utils import select_rows, insert_rows

def load_records():

    query = 'select distinct currency from "STAGING".price_history'

    currencies = select_rows(query)

    return None
