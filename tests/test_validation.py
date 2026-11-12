from src.dataforge.validation import (
    find_missing_values,
    find_duplicates,
    validate_records
)


def test_find_missing_values():
    records = [
        {"name": "Alice", "age": "20"},
        {"name": "", "age": "21"},
        {"name": "Charlie", "age": ""}
    ]

    issues = find_missing_values(records)

    assert len(issues) == 2
    assert issues[0]["column"] == "name"
    assert issues[1]["column"] == "age"


def test_find_duplicates():
    records = [
        {"name": "Alice", "age": "20"},
        {"name": "Bob", "age": "21"},
        {"name": "Alice", "age": "20"}
    ]

    duplicates = find_duplicates(records)

    assert len(duplicates) == 1
    assert duplicates[0]["row"] == 3


def test_validate_records():
    records = [
        {"name": "Alice", "age": "20"},
        {"name": "", "age": "21"},
        {"name": "Alice", "age": "20"}
    ]

    results = validate_records(records)

    assert len(results["missing_values"]) == 1
    assert len(results["duplicates"]) == 1