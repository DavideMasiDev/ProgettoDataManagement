from utils.db_utils import select_rows, insert_rows

def load_records():

    query = 'select distinct currency as currency_code from "STAGING".price_history'
    currencies = select_rows(query)

    currency_name = {"EUR": "Euro", "USD": "Dollaro Statunitense", "GBP": "Sterlina Britannica"}

    currencies["currency_name"] = currencies["currency_code"].map(currency_name)

    insert_rows("DWH", "currency", currencies)

    return None


def main():
    load_records()

if __name__ == '__main__':
    main()
