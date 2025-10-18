import sys
from load_staging import load_staging


def main():
    anno, mese, _primo_caricamento = sys.argv[1:]
    primo_caricamento = _primo_caricamento == "y"

    load_staging(anno, mese, primo_caricamento)

if __name__ == "__main__":
    main()