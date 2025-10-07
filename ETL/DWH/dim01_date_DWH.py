from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import pandas as pd


DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steam_dwh"

TABLE_NAME = "date"
SCHEMA_NAME = "DWH"

def load_records(start_date: datetime, end_date: datetime):
    records = []

    delta = timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        records.append({
            "date": current_date.date(),
            "year": current_date.year,
            "month": current_date.month,
            "day": current_date.day,
            "day_of_week": current_date.isoweekday(),
            "day_name": current_date.strftime("%A"),
            "month_name": current_date.strftime("%B")
        })
        current_date += delta

    # Chiamata al db per caricare le date generate

    # 1) Load and normalize
    df = pd.DataFrame(records, columns=["date", "year", "month", "day", "day_of_week", "day_name", "month_name"])
    print(f"* Records parsed: {len(df)}")

    # 2) Save CSV (staging)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"* CSV creato: {OUTPUT_FILE}")

    # 3) Connect to Postgres
    engine = create_engine(DB_URI)

    # 4) Carico dati in Postgres
    df.to_sql(TABLE_NAME, engine, schema=SCHEMA_NAME, if_exists="append", index=False, method="multi", chunksize=5000)
    print(f"* Inseriti {len(df)} record nella tabella '{TABLE_NAME}'")



def main():
    print("Loading DIM01_DATE_DWH...")
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2030, 12, 31)  
    load_records(start_date, end_date)
