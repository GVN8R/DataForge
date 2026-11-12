from src.dataforge.ingestion import read_csv


def main():
    records = read_csv("data/raw/sample.csv")

    for record in records:
        print(record)


if __name__ == "__main__":
    main()