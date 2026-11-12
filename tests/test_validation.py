from src.dataforge.validation import (
    find_missing_values,
    find_duplicates,
    validate_records,
    generate_quality_report,
    find_invalid_numbers,
    validate_with_rules
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


def test_find_invalid_numbers():
    records = [
        {"temperature": "42.5"},
        {"temperature": "unknown"},
        {"temperature": "38.2"},
        {"temperature": "abc"}
    ]

    issues = find_invalid_numbers(records, ["temperature"])

    assert len(issues) == 2
    assert issues[0]["row"] == 2
    assert issues[0]["value"] == "unknown"
    assert issues[1]["value"] == "abc"


def test_find_invalid_numbers_ignores_missing_values():
    records = [
        {"temperature": ""},
        {"temperature": "42.5"}
    ]

    issues = find_invalid_numbers(records, ["temperature"])

    assert issues == []


def test_find_invalid_numbers_multiple_columns():
    records = [
        {"temperature": "unknown", "precipitation": "rain"},
        {"temperature": "42.5", "precipitation": "0.2"}
    ]

    issues = find_invalid_numbers(
        records,
        ["temperature", "precipitation"]
    )

    assert len(issues) == 2


def test_validate_with_rules():
    records = [
        {"date": "2026-01-01", "temperature": "42.5"},
        {"date": "2026-01-02", "temperature": "unknown"},
        {"date": "2026-01-03", "temperature": "38.2"}
    ]

    rules = {
        "required_columns": ["date", "temperature"],
        "numeric_columns": ["temperature"],
        "unique_columns": ["date"]
    }

    results = validate_with_rules(records, rules)

    assert len(results["missing_values"]) == 0
    assert len(results["duplicates"]) == 0
    assert len(results["invalid_numbers"]) == 1


def test_validate_with_empty_rules():
    records = [
        {"name": "Alice"},
        {"name": "Bob"}
    ]

    results = validate_with_rules(records, {})

    assert results["invalid_numbers"] == []