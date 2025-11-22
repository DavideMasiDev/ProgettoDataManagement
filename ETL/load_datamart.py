from DATAMART.date_DM import load_records as load_records_date
from DATAMART.shop_DM import load_records as load_records_shop
from DATAMART.genres_DM import load_records as load_records_genres
from DATAMART.currency_DM import load_records as load_records_currency
from DATAMART.steam_game_DM import load_records as load_records_steam_game
from DATAMART.player_DM import load_records as load_records_player
from DATAMART.developer_DM import load_records as load_records_developer
from DATAMART.deal_fact_DM import load_records as load_records_deal_fact
from DATAMART.bridge_developer_DM import load_records as load_records_bridge_developer
from DATAMART.bridge_genre_DM import load_records as load_records_bridge_genre
from DATAMART.player_region_fact_DM import load_records as load_records_player_region_fact
from DATAMART.game_statistics_fact_DM import load_records as load_records_game_statistics_fact
from utils.db_utils import truncate_table


def load_datamart(data_inizio_periodo, data_fine_periodo):
    """data_inizio_periodo: stringa in formato 'YYYY-MM-DD'
        data_inizio_periodo: stringa in formato 'YYYY-MM-DD'"""

    truncate_table("DATAMART", "bridge_genre")
    truncate_table("DATAMART", "bridge_developer")
    truncate_table("DATAMART", "steam_game")
    truncate_table("DATAMART", "developer")
    truncate_table("DATAMART", "player")
    truncate_table("DATAMART", "date")
    truncate_table("DATAMART", "shop")
    truncate_table("DATAMART", "currency")
    truncate_table("DATAMART", "genre")

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
    print("Loading DATAMART deals")
    load_records_deal_fact(data_inizio_periodo, data_fine_periodo)
    print("Loading DATAMART bridge_developer")
    load_records_bridge_developer(data_inizio_periodo, data_fine_periodo)
    print("Loading DATAMART bridge_genre")
    load_records_bridge_genre(data_inizio_periodo, data_fine_periodo)
    print("Loading DATAMART player_region_fact")
    load_records_player_region_fact(data_inizio_periodo, data_fine_periodo)
    print("Loading DATAMART game_statistics_fact")
    load_records_game_statistics_fact(data_inizio_periodo, data_fine_periodo)


    return None


def main():
    load_datamart('2025-08-01', '2025-08-31')

if __name__ == "__main__":
    main()