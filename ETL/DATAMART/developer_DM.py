from utils.db_utils import insert_rows, select_rows, truncate_table

def load_records():

    query_developer_dwh = 'select developer_name from "DWH".developer'
    query_developer_dwh = select_rows(query_developer_dwh)

    truncate_table("DATAMART", "developer")
    insert_rows("DATAMART", "developer", query_developer_dwh)

    return None