from DATAMART.date_DM import load_records as load_records_date
from DATAMART.shop_DM import load_records as load_records_shop
from DATAMART.genres_DM import load_records as load_records_genres
from DATAMART.currency_DM import load_records as load_records_currency
from DATAMART.steam_game_DM import load_records as load_records_steam_game
from DATAMART.player_DM import load_records as load_records_player
from DATAMART.developer_DM import load_records as load_records_developer


def load_datamart(data_inizio_periodo, data_fine_periodo):

    # Caricamento tabelle statiche

    print("Loading DATAMART date")
    load_records_date()
    print("Loading DATAMART shop")
    load_records_shop()
    print("Loading DATAMART genres")
    load_records_genres()
    print("Loading DATAMART currency")
    load_records_currency()
    print("Loading DATAMART steam game")
    load_records_steam_game()
    print("Loading DATAMART player")
    load_records_player()
    print("Loading DATAMART developer")
    load_records_developer()


    return None


def main():
    load_datamart('2020/01/01', '2020/01/02')

if __name__ == "__main__":
    main()