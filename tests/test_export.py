import csv
import pytest
from src.dataforge.export import write_csv


def test_write_csv_creates_valid_file(tmp_path):
    records = [
        {"date": "2026-01-01", "temperature": 72.0},
        {"date": "2026-01-02", "temperature": 75.0}
    ]

    output_path = tmp_path / "processed" / "weather.csv"

    write_csv(records, output_path)

    with output_path.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        result = list(csv.DictReader(file))

    assert len(result) == 2
    assert result[0]["date"] == "2026-01-01"
    assert result[0]["temperature"] == "72.0"


def test_write_csv_rejects_empty_dataset(tmp_path):
    output_path = tmp_path / "empty.csv"

    with pytest.raises(ValueError):
        write_csv([], output_path)


def test_write_csv_does_not_modify_records(tmp_path):
    records = [{"city": "Rolla", "temperature": 72.0}]
    original = [record.copy() for record in records]

    write_csv(records, tmp_path / "weather.csv")

    assert records == original