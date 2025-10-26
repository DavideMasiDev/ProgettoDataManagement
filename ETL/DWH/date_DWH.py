from datetime import datetime, timedelta
import pandas as pd
from utils.db_utils import insert_rows, find_new_records, select_rows

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

    query = 'select full_date::date from "DWH".date'
    date_dwh = select_rows(query)

    df = find_new_records(df, date_dwh, ["full_date"] )

    insert_rows("DWH", "date", df)
