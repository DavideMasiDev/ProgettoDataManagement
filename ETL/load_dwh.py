from DWH.date_DWH import load_records as load_record_date
from DWH.currency_DWH import load_records as load_record_currency
from DWH.developer_DWH import load_records as load_record_developer
from DWH.genres_DWH import load_records as load_record_genres
from DWH.player_DWH import load_records as load_record_player
from DWH.shop_DWH import load_records as load_record_shop
from DWH.steam_game_DWH import load_records as load_record_steam_game
from DWH.bridge_genre_DWH import load_records as load_record_bridge_genres
from DWH.bridge_developer_DWH import load_records as load_record_bridge_developer
from DWH.deal_fact_DWH import load_records as load_record_deal
from DWH.game_statistics_fact import load_records as load_record_game_statistics_fact
from DWH.player_region_fact_DWH import load_records as load_record_player_region_fact
from datetime import datetime
from calendar import monthrange




def load_dwh(anno, mese, primo_caricamento):

    mapping_mese = {
        'GENNAIO': '01',
        'FEBBRAIO': '02',
        'MARZO': '03',
        'APRILE': '04',
        'MAGGIO': '05',
        'GIUGNO': '06',
        'LUGLIO': '07',
        'AGOSTO': '08',
        'SETTEMBRE': '09',
        'OTTOBRE': '10',
        'NOVEMBRE': '11',
        'DICEMBRE': '12',
    }

    mapping_mese_precedente = {
        'GENNAIO': '12',
        'FEBBRAIO': '01',
        'MARZO': '02',
        'APRILE': '03',
        'MAGGIO': '04',
        'GIUGNO': '05',
        'LUGLIO': '06',
        'AGOSTO': '07',
        'SETTEMBRE': '08',
        'OTTOBRE': '09',
        'NOVEMBRE': '10',
        'DICEMBRE': '11',
    }

    last_day_month = monthrange(int(anno), int(mapping_mese[mese]))[1]
    last_day_precedent_month = monthrange(int(anno), int(mapping_mese_precedente[mese]))[1]

    loading_date = datetime.strptime('01/' + mapping_mese[mese] + '/' + anno, "%d/%m/%Y")
    if primo_caricamento:
        start_date = datetime.strptime('01/01/1950', "%d/%m/%Y")
    else:
        start_date = loading_date
    end_date = datetime.strptime(str(last_day_month) + '/' + mapping_mese[mese] + '/' + anno, "%d/%m/%Y")

    if mapping_mese_precedente[mese]!='12':
        end_date_precedent_month = datetime.strptime(str(last_day_precedent_month) + '/' + mapping_mese_precedente[mese] + '/' + anno, "%d/%m/%Y")
    else:
        end_date_precedent_month = datetime.strptime(str(last_day_precedent_month) + '/' + mapping_mese_precedente[mese] + '/' + (anno-1), "%d/%m/%Y")

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
    load_record_bridge_genres(loading_date, end_date_precedent_month)
    print("Loading DWH bridge developer")
    load_record_bridge_developer(loading_date, end_date_precedent_month)
    print("Loading DWH deal fact")
    load_record_deal()
    print("Loading DWH game statistics fact")
    load_record_game_statistics_fact(start_date, end_date_precedent_month)
    print("Loading DWH player region fact")
    load_record_player_region_fact(loading_date)

    return None


def main():
    load_dwh('2025', 'DICEMBRE', True)


if __name__ == '__main__':
    main()