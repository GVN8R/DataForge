from src.dataforge.validation import (
    find_missing_values,
    find_duplicates,
    validate_records,
    generate_quality_report
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


def test_quality_report_with_issues():
    records = [
        {"name": "Alice", "age": "20"},
        {"name": "", "age": "21"},
        {"name": "Alice", "age": "20"}
    ]

    report = generate_quality_report(records)

    assert report["total_records"] == 3
    assert report["missing_values"] == 1
    assert report["duplicate_records"] == 1
    assert report["total_issues"] == 2
    assert report["passed"] is False


def test_quality_report_without_issues():
    records = [
        {"name": "Alice", "age": "20"},
        {"name": "Bob", "age": "21"}
    ]

    report = generate_quality_report(records)

    assert report["total_records"] == 2
    assert report["total_issues"] == 0
    assert report["passed"] is True