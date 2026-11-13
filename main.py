from src.dataforge.ingestion import read_csv
from src.dataforge.rules import WEATHER_RULES
from src.dataforge.validation import (
    generate_full_quality_report,
    format_quality_report
)


def main():
    records = read_csv("data/raw/sample.csv")

    report = generate_full_quality_report(records, WEATHER_RULES)

    print(format_quality_report(report))


if __name__ == "__main__":
    main()