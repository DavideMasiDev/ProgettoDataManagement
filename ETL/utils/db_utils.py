from pandas import DataFrame, merge
from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:dm2025@localhost:5432/steamdb"

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

def select_rows(query) -> DataFrame:

    engine = connect_db(DB_URI)
    connection = engine.connect()

    query_result = connection.execute(text(query))
    columns_name = query_result.keys()

    result = DataFrame(query_result.fetchall())
    if result.empty:
        for elem in columns_name:
            result[elem] = []
    else:
        result.columns = columns_name

    return result

def find_new_records(df_staging, df_dwh, key_column):

    if isinstance(key_column, str):
        key_column = [key_column]

    merged_df = merge(
        df_staging,
        df_dwh[key_column],
        on=key_column,
        how='left',
        indicator=True
    )

    new_rows = merged_df[merged_df['_merge'] == 'left_only']

    df_to_set = new_rows[df_staging.columns]

    return df_to_set

def truncate_table(schema, table):
    engine = connect_db(DB_URI)
    connection = engine.connect()

    query = f'TRUNCATE TABLE "{schema}".{table} CONTINUE IDENTITY RESTRICT'

    connection.execute(text(query))
    connection.commit()
