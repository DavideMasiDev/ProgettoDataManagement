from utils.db_utils import select_rows, insert_rows, find_new_records
import pandas as pd

def load_records():

    query = 'select distinct developers from "STAGING".released_game'
    developers = select_rows(query)

    developers_list_to_split = developers.values.tolist()
    developers_list = []

    for elem in developers_list_to_split:
        if elem[0] is not None:
            for developer in elem[0].split(";"):
                if developer not in developers_list:
                    developers_list.append(developer)

    developers = pd.DataFrame(developers_list, columns=["developer_name"])

    # Recuperiamo i record già inseriti in DWH in modo da non creare duplicati nella tabella,
    # essendo quest'ultima solamente una tipologica.
    # Verranno inseriti solamente currency che non erano già presenti.

    query = 'select developer_name from "DWH".developer'
    dwh_developers = select_rows(query)

    developers = find_new_records(developers, dwh_developers, ['developer_name'])

    insert_rows("DWH", "developer", developers)

    return None
