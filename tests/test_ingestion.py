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

    with pytest.raises(ValueError, match="number of values"):
        read_csv(file)



def test_rejects_invalid_utf8_encoding(tmp_path):
    file_path = tmp_path / "invalid.csv"
    file_path.write_bytes(b"name,age\nAlice,\xff")

    with pytest.raises(ValueError, match="invalid UTF-8"):
        read_csv(file_path)


def test_rejects_rows_with_too_few_values(tmp_path):
    file_path = tmp_path / "short.csv"
    file_path.write_text(
        "name,age,city\nAlice,20\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="inconsistent"):
        read_csv(file_path)


def test_rejects_whitespace_only_file(tmp_path):
    file_path = tmp_path / "whitespace.csv"
    file_path.write_text("   \n   \n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_csv(file_path)


def test_strips_column_names(tmp_path):
    file_path = tmp_path / "headers.csv"
    file_path.write_text(
        " name , age \nAlice,20\n",
        encoding="utf-8"
    )

    result = read_csv(file_path)

    assert result == [{"name": "Alice", "age": "20"}]
