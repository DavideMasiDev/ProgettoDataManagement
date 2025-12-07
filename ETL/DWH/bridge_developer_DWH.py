from utils.db_utils import select_rows, find_new_records, insert_rows, update_table
import pandas as pd
import datetime

def load_records(dat_ini_val, dat_fin_val):
    dat_ini_val = dat_ini_val.strftime('%Y-%m-%d')
    dat_fin_val = dat_fin_val.strftime('%Y-%m-%d')

    query = ('select steam_game_pk, developers '
             'from "STAGING".released_game rg '
             'join "DWH".steam_game sg on (rg.steam_appid = sg.steam_appid)')
    developers_per_game = select_rows(query)
    developers_per_game_list = developers_per_game.values.tolist()

    query = 'select developer_pk, developer_name from "DWH".developer'
    developers = select_rows(query)

    query = 'select steam_game_pk, developer_pk from "DWH".bridge_developer'
    bridge_developer_df_dwh = select_rows(query)

    bridge_developer = []
    for elem in developers_per_game_list:
        if elem[1] is not None:
            for developer in elem[1].split(";"):
                bridge_developer.append((elem[0], developers[developers['developer_name'] == developer]['developer_pk'].values[0], dat_ini_val, '9999-12-31'))

    bridge_developer_df = pd.DataFrame(bridge_developer, columns=['steam_game_pk', 'developer_pk', 'dat_ini_val', 'dat_fin_val'])

    bridge_developer_new = find_new_records(bridge_developer_df, bridge_developer_df_dwh, ['steam_game_pk', 'developer_pk'])

    insert_rows("DWH", "bridge_developer", bridge_developer_new)

    # Recupera tutti i record presenti in DWH ma non nello staging --> Il mapping gioco - developer
    # non esiste più nel periodo che sta considerando lo staging e deve essere quindi chiuso in DWH

    bridge_developer_close = find_new_records(bridge_developer_df_dwh, bridge_developer_df, ['steam_game_pk', 'developer_pk'])
    bridge_developer_close_list = bridge_developer_close.values.tolist()

    for elem in bridge_developer_close_list:
        update_query = ('update "DWH".bridge_developer set dat_fin_val=' + "'" + dat_fin_val + "'" +
                        ' where steam_game_pk = ' + str(elem[0]) + ' and developer_pk = ' + str(elem[1]))

        update_table(update_query)


    return None
