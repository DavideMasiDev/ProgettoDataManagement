from DWH.date_DWH import load_records as load_record_date
from DWH.currency_DWH import load_records as load_record_currency
from DWH.developer_DWH import load_records as load_record_developer
from DWH.genres_DWH import load_records as load_record_genres
from DWH.player_DWH import load_records as load_record_player
from DWH.shop_DWH import load_records as load_record_shop
from DWH.steam_game_DWH import load_records as load_record_steam_game
from DWH.bridge_genre_DWH import load_records as load_record_bridge_genres
from DWH.bridge_developer_DWH import load_records as load_record_bridge_developer
from datetime import datetime



def load_dwh(start_date, end_date):

    print("Loading DWH date")
    load_record_date(start_date, end_date)
    print("Loading DWH currency")
    load_record_currency()
    print("Loading DWH developer")
    load_record_developer()
    print("Loading DWH genres")
    load_record_genres()
    print("Loading DWH player")
    load_record_player()
    print("Loading DWH shop")
    load_record_shop()
    print("Loading DWH steam game")
    load_record_steam_game()
    print("Loading DWH bridge genres")
    load_record_bridge_genres()
    print("Loading DWH bridge developer")
    load_record_bridge_developer()

    return None


def main():
    start_date = datetime.strptime('01/01/2025', '%d/%m/%Y')
    end_date = datetime.strptime('30/06/2025', '%d/%m/%Y')

    load_dwh(start_date, end_date)


if __name__ == '__main__':
    main()