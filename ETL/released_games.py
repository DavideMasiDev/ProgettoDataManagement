import pandas as pd
import re
from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/steamdb"
RELEASED_GAMES_SOURCE = "raw_sources/aug-25-released-games.csv"
RELEASED_DLCS_SOURCE = "raw_sources/aug-25-released-dlcs.csv"
SCHEMA_NAME = "STAGING"

# Normalizza i valori stringa "undefined", "n/a", "none", "null", "nan" → None
def normalize_undefined(val):
    if isinstance(val, str):
        v = val.strip().lower()
        if v in ["undefined", "n/a", "none", "null", "nan", ""]:
            return None
    return val

def load_released_games_to_db(csv_path: str, db_uri: str, schema_name:str, table_name: str = "released_game") -> None:

    print(f"* Lettura CSV da {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)

    # Colonne valide secondo lo schema del DB
    valid_columns = [
        "name", "steam_appid", "short_description", "required_age", "controller_support",
        "supported_languages", "developers", "publishers", "platforms", "categories",
        "genres", "release_date", "followers", "estimated_wishlists", "tags", "price",
        "estimated_revenue", "estimated_units", "currency", "owners", "average_forever",
        "average_2weeks", "median_forever", "median_2weeks", "concurrent_users",
        "total_positive", "total_negative", "total_reviews"
    ]

    # Mantieni solo le colonne che esistono nel DB
    df = df[[col for col in df.columns if col in valid_columns]].copy()

    print("* Pulizia e conversione dati...")

    # Normalizza tutti i valori stringa: "undefined" -> None
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(normalize_undefined)

    # Normalizza booleana
    if "controller_support" in df.columns:
        df["controller_support"] = (
            df["controller_support"]
            .astype(str)
            .str.lower()
            .isin(["true", "1", "yes", "full"])
        )

    # Conversione numeri
    numeric_cols = [
        "steam_appid", "average_forever", "average_2weeks",
        "median_forever", "median_2weeks", "concurrent_users",
        "total_positive", "total_negative", "total_reviews"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # Conversione date
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.date

    # Pulizia required_age -> solo numeri e max 2 caratteri
    if "required_age" in df.columns:
        df["required_age"] = (
            df["required_age"]
            .astype(str)
            .apply(lambda x: re.sub(r"\D", "", x)[:2] if pd.notna(x) else None)
        )
        # Se stringa vuota dopo la pulizia, metti NULL
        df.loc[df["required_age"] == "", "required_age"] = None

    # Rimuovi record con valori NULL nei campi obbligatori
    not_null_fields = ["name", "steam_appid", "release_date"]
    before = len(df)
    df = df.dropna(subset=not_null_fields)
    after = len(df)
    skipped = before - after

    if skipped > 0:
        print(f"* Ignorati {skipped} record con valori NULL nei campi NOT NULL.")

    # Connessione al DB
    print("* Connessione a Postgres...")
    engine = create_engine(db_uri)

    # Inserimento dati
    print(f"* Inserimento di {len(df)} record nella tabella '{table_name}'...")
    df.to_sql(table_name, engine, schema=schema_name, if_exists="append", index=False, chunksize=5000)
    print(f"* Completato: {len(df)} record inseriti in '{table_name}'.")


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    print(f"Carico i giochi rilasciati")
    load_released_games_to_db(RELEASED_GAMES_SOURCE, DB_URI, SCHEMA_NAME)
    print(f"\n--------------------\n")
    print(f"Carico i dlc rilasciati")
    load_released_games_to_db(RELEASED_DLCS_SOURCE, DB_URI, SCHEMA_NAME)
