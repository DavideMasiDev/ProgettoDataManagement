import sys
from load_staging import load_staging


def main():
    anno, mese = sys.argv[1:]
    load_staging(anno, mese)

if __name__ == "__main__":
    main()