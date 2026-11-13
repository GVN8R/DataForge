from src.dataforge.validation import (
    find_missing_values,
    find_duplicates,
    validate_records,
    generate_quality_report,
    find_invalid_numbers,
    validate_with_rules,
    find_missing_columns,
    find_duplicate_values,
    generate_full_quality_report,
    format_quality_report
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


def test_find_missing_columns():
    records = [
        {"date": "2026-01-01", "temperature": "42.5"}
    ]

    issues = find_missing_columns(
        records,
        ["date", "temperature", "precipitation"]
    )

    assert len(issues) == 1
    assert issues[0]["column"] == "precipitation"


def test_find_missing_columns_empty_dataset():
    issues = find_missing_columns(
        [],
        ["date", "temperature"]
    )

    assert len(issues) == 2


def test_find_missing_columns_all_present():
    records = [
        {"date": "2026-01-01", "temperature": "42.5"}
    ]

    issues = find_missing_columns(
        records,
        ["date", "temperature"]
    )

    assert issues == []


def test_validate_with_rules_detects_missing_columns():
    records = [
        {"date": "2026-01-01"}
    ]

    rules = {
        "required_columns": ["date", "temperature"],
        "numeric_columns": ["temperature"]
    }

    results = validate_with_rules(records, rules)

    assert len(results["missing_columns"]) == 1
    assert results["missing_columns"][0]["column"] == "temperature"


def test_find_duplicate_values():
    records = [
        {"date": "2026-01-01", "temperature": "42"},
        {"date": "2026-01-02", "temperature": "38"},
        {"date": "2026-01-01", "temperature": "45"}
    ]

    issues = find_duplicate_values(records, ["date"])

    assert len(issues) == 1
    assert issues[0]["row"] == 3
    assert issues[0]["column"] == "date"


def test_find_duplicate_values_multiple_columns():
    records = [
        {"date": "2026-01-01", "station": "A"},
        {"date": "2026-01-02", "station": "A"},
        {"date": "2026-01-01", "station": "B"}
    ]

    issues = find_duplicate_values(
        records,
        ["date", "station"]
    )

    assert len(issues) == 2


def test_validate_with_rules_detects_duplicate_values():
    records = [
        {"date": "2026-01-01", "temperature": "42"},
        {"date": "2026-01-01", "temperature": "45"}
    ]

    rules = {
        "required_columns": ["date", "temperature"],
        "numeric_columns": ["temperature"],
        "unique_columns": ["date"]
    }

    results = validate_with_rules(records, rules)

    assert len(results["duplicate_values"]) == 1


def test_full_quality_report():
    records = [
        {"date": "2026-01-01", "temperature": "42"},
        {"date": "2026-01-01", "temperature": "unknown"},
        {"date": "2026-01-03", "temperature": ""}
    ]

    rules = {
        "required_columns": ["date", "temperature"],
        "numeric_columns": ["temperature"],
        "unique_columns": ["date"]
    }

    report = generate_full_quality_report(records, rules)

    assert report["total_records"] == 3
    assert report["total_issues"] == 3
    assert report["passed"] is False


def test_full_quality_report_clean_dataset():
    records = [
        {"date": "2026-01-01", "temperature": "42"},
        {"date": "2026-01-02", "temperature": "38"}
    ]

    rules = {
        "required_columns": ["date", "temperature"],
        "numeric_columns": ["temperature"],
        "unique_columns": ["date"]
    }

    report = generate_full_quality_report(records, rules)

    assert report["total_records"] == 2
    assert report["total_issues"] == 0
    assert report["passed"] is True


def test_format_quality_report():
    report = {
        "total_records": 100,
        "issue_counts": {
            "missing_columns": 0,
            "missing_values": 3,
            "duplicates": 2,
            "invalid_numbers": 1,
            "duplicate_values": 0
        },
        "total_issues": 6,
        "passed": False
    }

    output = format_quality_report(report)

    assert "DATAFORGE QUALITY REPORT" in output
    assert "Total records: 100" in output
    assert "Missing Values: 3" in output
    assert "Total issues: 6" in output
    assert "Status: ISSUES FOUND" in output


def test_format_clean_quality_report():
    report = {
        "total_records": 50,
        "issue_counts": {
            "missing_columns": 0,
            "missing_values": 0,
            "duplicates": 0,
            "invalid_numbers": 0,
            "duplicate_values": 0
        },
        "total_issues": 0,
        "passed": True
    }

    output = format_quality_report(report)

    assert "Total issues: 0" in output
    assert "Status: PASSED" in output


def test_missing_values_detects_whitespace():
    records = [
        {"name": "Alice"},
        {"name": "   "}
    ]

    issues = find_missing_values(records)

    assert len(issues) == 1
    assert issues[0]["row"] == 2


def test_duplicate_values_ignores_whitespace():
    records = [
        {"date": "2026-01-01"},
        {"date": "   "},
        {"date": "2026-01-02"}
    ]

    issues = find_duplicate_values(records, ["date"])

    assert issues == []


def test_invalid_numbers_detects_whitespace():
    records = [
        {"temperature": "   "},
        {"temperature": "42.5"}
    ]

    issues = find_invalid_numbers(records, ["temperature"])

    assert issues == []


def test_quality_report_empty_dataset():
    report = generate_full_quality_report(
        [],
        {
            "required_columns": ["date"],
            "numeric_columns": ["temperature"],
            "unique_columns": ["date"]
        }
    )

    assert report["total_records"] == 0
    assert report["total_issues"] == 1
    assert report["passed"] is False