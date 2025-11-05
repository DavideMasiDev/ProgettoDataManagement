from utils.db_utils import select_rows, insert_rows, find_new_records


def load_records():

    query = ('select d.date_pk as deal_date_pk, sg.steam_game_pk, c.currency_pk, s.shop_pk, ph.price, ph.regular_price, ph.deal'
              ' from "STAGING".price_history ph'
              ' join "DWH".steam_game sg on sg.steam_appid = ph.steam_appid'
              ' join "DWH".date d on d.full_date::date = ph."timestamp"'
              ' join "DWH".currency c on c.currency_code = ph.currency'
              ' join "DWH".shop s on s.shop_name = ph.shop')

    deals = select_rows(query)

    insert_rows('DWH', 'deal_fact', deals)

    return None

