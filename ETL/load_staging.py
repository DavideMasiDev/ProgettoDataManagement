from STAGING.game_player_region_STG import load_records as load_records_game_player_region
from STAGING.raw_data_STG import load_records as load_records_raw_data
from STAGING.released_games_STG import load_records as load_records_released_games
from STAGING.SCRAPER.price_history_scraper_STG import load_records as load_records_price_history



def load_staging(anno, mese):

    input_path_raw_data = "raw_sources/RAW_DATA/" + anno + "/" +  mese + "/raw"
    input_path_game_player_region = "raw_sources/GAME_PLAYER_REGION/" + anno + "/" + mese + "/game_player_regions.csv"
    input_path_released_game_game = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/game.csv"
    input_path_released_game_dlc = "raw_sources/RELEASED_GAMES/" + anno + "/" + mese + "/dlc.csv"

    games = load_records_raw_data(input_path_raw_data)
    load_records_game_player_region(input_path_game_player_region)
    load_records_released_games(input_path_released_game_game, input_path_released_game_dlc)
    load_records_price_history(games)

    return None