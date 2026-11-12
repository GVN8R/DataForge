import pytest
from src.dataforge.ingestion import read_csv


def test_read_valid_csv(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text(
        "name,age\nAlice,20\nBob,21\n",
        encoding="utf-8"
    )

    records = read_csv(file)

    assert len(records) == 2
    assert records[0]["name"] == "Alice"
    assert records[1]["age"] == "21"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        read_csv("DNE.csv")


def test_empty_csv(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError):
        read_csv(file)


def test_headers_only_csv(tmp_path):
    file = tmp_path / "headers.csv"
    file.write_text("name,age\n", encoding="utf-8")

    records = read_csv(file)

    assert records == []