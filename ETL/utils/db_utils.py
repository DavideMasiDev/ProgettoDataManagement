from pandas import DataFrame
from sqlalchemy import create_engine

DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steamdb"

def connect_db(db_uri):
    engine = create_engine(db_uri)
    return engine

def insert_rows(schema, table, records: DataFrame):

    engine = connect_db(DB_URI)

    try:
        records.to_sql(table, engine, schema=schema, if_exists="append", index=False, method="multi", chunksize=5000)
    except  Exception as e:
        print("Errore durante il caricamento della tabella " + schema + "." + table + ":" + str(e))

    return None

