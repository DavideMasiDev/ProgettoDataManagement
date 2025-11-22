from utils.db_utils import select_rows, find_new_records, insert_rows, update_table
import pandas as pd
import datetime

def load_records():

    query = ('select steam_game_pk, tags '
             'from "STAGING".released_game rg '
             'join "DWH".steam_game sg on (rg.steam_appid = sg.steam_appid)')
    genres_per_game = select_rows(query)
    genres_per_game_list = genres_per_game.values.tolist()

    query = 'select genre_pk, genre_name from "DWH".genre'
    genres = select_rows(query)

    query = 'select steam_game_pk, genre_pk from "DWH".bridge_genre'
    bridge_genre_df_dwh = select_rows(query)

    bridge_genre = []
    for elem in genres_per_game_list:
        if elem[1] is not None:
            for genre in elem[1].split(";"):
                bridge_genre.append((elem[0], genres[genres['genre_name'] == genre]['genre_pk'].values[0], '01-01-0001', '9999-12-31'))

    bridge_genre_df = pd.DataFrame(bridge_genre, columns=['steam_game_pk', 'genre_pk', 'dat_ini_val', 'dat_fin_val'])

    bridge_genre_new = find_new_records(bridge_genre_df, bridge_genre_df_dwh, ['steam_game_pk', 'genre_pk'])

    insert_rows("DWH", "bridge_genre", bridge_genre_new)

    # Recupera tutti i record presenti in DWH ma non nello staging --> Il mapping gioco - developer
    # non esiste più nel periodo che sta considerando lo staging e deve essere quindi chiuso in DWH

    bridge_genre_close = find_new_records(bridge_genre_df_dwh, bridge_genre_df, ['steam_game_pk', 'genre_pk'])
    bridge_genre_close_list = bridge_genre_close.values.tolist()

    for elem in bridge_genre_close_list:
        update_query = ('update "DWH".bridge_genre set dat_fin_val='+ "'" + datetime.date.today().strftime('%Y-%m-%d') + "'" +
                        ' where steam_game_pk = ' + str(elem[0]) + ' and genre_pk = ' + str(elem[1]))

        update_table(update_query)


    return None
