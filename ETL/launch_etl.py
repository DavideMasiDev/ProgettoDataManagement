import sys
from load_staging import load_staging
from load_dwh import load_dwh
from load_datamart import load_datamart

# TODO: add your key here
SCRAPER_API_KEY = "INSERT_YOUR_API_KEY_HERE"

def main():
    anno, mese, _primo_caricamento = sys.argv[1:]
    primo_caricamento = _primo_caricamento == "y"

    if SCRAPER_API_KEY == "your_api_key":
        print(f"\n-------------------------------------------------------")
        print(f"[ATTENZIONE] Inserire l'API-KEY nel file launch_etl.py!")
        print(f"-------------------------------------------------------\n")
        return

    print("Inizio caricamento STAGING: " + mese + " " + anno)
    load_staging(anno, mese, primo_caricamento, SCRAPER_API_KEY)
    print("Fine caricamento STAGING: " + mese + " " + anno)

    print("Inizio caricamento DWH: " + mese + " " + anno)
    load_dwh(anno, mese, primo_caricamento)
    print("Fine caricamento DWH: " + mese + " " + anno)

if __name__ == "__main__":
    main()