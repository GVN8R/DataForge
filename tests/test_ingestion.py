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


def test_duplicate_headers(tmp_path):
    file = tmp_path / "duplicate.csv"
    file.write_text("name,name\nAlice,Smith\n", encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate"):
        read_csv(file)


def test_empty_header(tmp_path):
    file = tmp_path / "empty_header.csv"
    file.write_text("name,\nAlice,20\n", encoding="utf-8")

    with pytest.raises(ValueError, match="empty column"):
        read_csv(file)


def test_extra_values_in_row(tmp_path):
    file = tmp_path / "extra.csv"
    file.write_text("name,age\nAlice,20,extra\n", encoding="utf-8")

    with pytest.raises(ValueError, match="more values"):
        read_csv(file)