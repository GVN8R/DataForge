from src.dataforge.ingestion import read_csv
from src.dataforge.validation import generate_quality_report


def main():
    records = read_csv("data/raw/sample.csv")

    report = generate_quality_report(records)

    print("\nDATA QUALITY REPORT")
    print("-------------------")
    print(f"Total records: {report["total_records"]}")
    print(f"Missing values: {report["missing_values"]}")
    print(f"Duplicates: {report["duplicate_records"]}")
    print(f"Total issues: {report["total_issues"]}")
    print(f"Passed: {report["passed"]}")


if __name__ == "__main__":
    main()