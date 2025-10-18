import sys
from load_staging import load_staging

# TODO: add your key here
SCRAPER_API_KEY = "your_api_key"

def main():
    anno, mese, _primo_caricamento = sys.argv[1:]
    primo_caricamento = _primo_caricamento == "y"

    if SCRAPER_API_KEY == "your_api_key":
        print(f"\n-------------------------------------------------------")
        print(f"!ATTENZIONE! Inserire l'API-KEY nel file launch_etl.py!")
        print(f"-------------------------------------------------------\n")
        return

    load_staging(anno, mese, primo_caricamento, SCRAPER_API_KEY)

if __name__ == "__main__":
    main()