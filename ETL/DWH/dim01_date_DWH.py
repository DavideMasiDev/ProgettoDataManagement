from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import pandas as pd
from utils.db_utils import insert_rows

def load_records(start_date: datetime, end_date: datetime):
    records = []

    delta = timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        records.append({
            "full_date": current_date.date(),
            "year": current_date.year,
            "month": current_date.month,
            "day": current_date.day,
            "day_of_week": current_date.isoweekday(),
            "day_name": current_date.strftime("%A"),
            "month_name": current_date.strftime("%B")
        })
        current_date += delta

    # Chiamata al db per caricare le date generate

    # Load and normalize
    df = pd.DataFrame(records, columns=["full_date", "year", "month", "day", "day_of_week", "day_name", "month_name"])
    print(f"* Records parsed: {len(df)}")

    insert_rows("DWH", "date", df)
