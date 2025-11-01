from utils.db_utils import select_rows, find_new_records, insert_rows, update_table
import datetime

def load_records():
    today = datetime.date.today().strftime('%Y-%m-%d')
    query = (f'select player_pk, steam_game_pk, \'{today}\' as dat_ini_val, \'9999-12-31\' as dat_fin_val'
             ' from "STAGING".game_player_region gpr'
             ' join "DWH".player p on gpr.player_steamid = p.player_steamid'
             ' join "DWH".steam_game sg on gpr.steam_appid = sg.steam_appid')
    players_for_game = select_rows(query)

    query = ('select player_pk, steam_game_pk, dat_ini_val, dat_fin_val'
             ' from "DWH".player_region_fact prf')
    player_region_fact = select_rows(query)

    new_records = find_new_records(players_for_game, player_region_fact, ['steam_game_pk', 'player_pk'])
    insert_rows("DWH", "player_region_fact", new_records)

    return None
