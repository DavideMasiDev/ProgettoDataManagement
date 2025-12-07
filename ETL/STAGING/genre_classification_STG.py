import pandas as pd
from utils.db_utils import insert_rows, find_new_records, select_rows, truncate_table

SCHEMA_NAME = 'STAGING'
TABLE_NAME = 'genre_classification'

def load_records(input_path):
    genre_classification_df = pd.read_csv(input_path)
    truncate_table(SCHEMA_NAME, TABLE_NAME)
    insert_rows(SCHEMA_NAME, TABLE_NAME, genre_classification_df)


