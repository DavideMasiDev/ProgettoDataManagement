from STAGING.game_player_region_STG import load_records as load_records_game_player_region
from STAGING.raw_data_STG import load_records as load_records_raw_data
from STAGING.released_games_STG import load_records as load_records_released_games
from STAGING.SCRAPER.price_history_scraper_STG import load_records as load_records_price_history
from STAGING.genre_classification_STG import load_records as load_records_genre_classification


def load_staging(anno, mese, primo_caricamento, apy_key):

    input_path_raw_data = "raw_sources/RAW_DATA/" + anno + "/" +  mese + "/raw"
    input_path_game_player_region = "raw_sources/GAME_PLAYER_REGION/" + anno + "/" + mese + "/game_player_regions.json"
    input_path_released_game_game = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/game.csv"
    input_path_released_game_dlc = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/dlc.csv"
    input_path_released_game_free_game = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/free-game.csv"
    input_path_released_game_free_dlc = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/free-dlc.csv"
    input_path_genre_classification = "raw_sources/MAPPING_DATA/genre_classification.csv"

    games = load_records_raw_data(input_path_raw_data)
    load_records_genre_classification(input_path_genre_classification)
    load_records_game_player_region(input_path_game_player_region)
    load_records_released_games(input_path_released_game_game,
                                input_path_released_game_dlc,
                                input_path_released_game_free_game,
                                input_path_released_game_free_dlc)
    load_records_price_history(games, primo_caricamento, apy_key)

    return None

def main():
    load_staging('2025', 'DICEMBRE', True)


if __name__ == '__main__':
    main()