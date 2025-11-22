from utils.db_utils import select_rows, insert_rows, find_new_records
import pandas as pd

def load_records():

    query = 'select distinct tags from "STAGING".released_game'
    genres = select_rows(query)

    genres_list_to_split = genres.values.tolist()
    genres_list = []

    for elem in genres_list_to_split:
        if elem[0] is not None:
            for genre in elem[0].split(";"):
                if genre not in genres_list:
                    genres_list.append(genre)

    genres = pd.DataFrame(genres_list, columns=["genre_name"])

    # Recuperiamo i record già inseriti in DWH in modo da non creare duplicati nella tabella,
    # essendo quest'ultima solamente una tipologica.
    # Verranno inseriti solamente currency che non erano già presenti.

    query = 'select genre_name from "DWH".genre'
    dwh_genres = select_rows(query)

    genres = find_new_records(genres, dwh_genres, ['genre_name'])

    insert_rows("DWH", "genre", genres)

    return None
