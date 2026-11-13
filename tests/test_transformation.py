import pytest
from src.dataforge.transformation import (
    normalize_column_names,
    normalize_text_values,
    normalize_missing_values,
    convert_numeric_columns
)


def test_normalize_column_names():
    records = [
        {
            " Temperature ": "42.5",
            " DATE ": "2026-01-01"
        }
    ]

    result = normalize_column_names(records)

    assert result == [
        {
            "temperature": "42.5",
            "date": "2026-01-01"
        }
    ]


def test_normalize_text_values():
    records = [
        {
            "city": "  Springfield  ",
            "temperature": " 42.5 "
        }
    ]

    result = normalize_text_values(records)

    assert result == [
        {
            "city": "Springfield",
            "temperature": "42.5"
        }
    ]


def test_normalize_empty_records():
    assert normalize_column_names([]) == []
    assert normalize_text_values([]) == []


def test_normalize_column_collision():
    records = [
        {
            "Temperature": "42",
            " temperature ": "45"
        }
    ]

    with pytest.raises(ValueError, match="collision"):
        normalize_column_names(records)


def test_normalize_missing_values():
    records = [
        {"temperature": "42.5"},
        {"temperature": ""},
        {"temperature": "N/A"},
        {"temperature": "unknown"},
        {"temperature": "null"}
    ]

    result = normalize_missing_values(records)

    assert result == [
        {"temperature": "42.5"},
        {"temperature": None},
        {"temperature": None},
        {"temperature": None},
        {"temperature": None}
    ]


def test_custom_missing_markers():
    records = [
        {"status": "not recorded"},
        {"status": "42"}
    ]

    result = normalize_missing_values(
        records,
        {"not recorded"}
    )

    assert result == [
        {"status": None},
        {"status": "42"}
    ]


def test_missing_value_normalization_preserves_non_strings():
    records = [
        {"temperature": 42.5},
        {"temperature": None}
    ]

    result = normalize_missing_values(records)

    assert result == records


def test_convert_numeric_columns():
    records = [
        {"temperature": "42.5", "city": "Springfield"},
        {"temperature": "38", "city": "Rolla"}
    ]

    result = convert_numeric_columns(
        records,
        ["temperature"]
    )

    assert result[0]["temperature"] == 42.5
    assert result[1]["temperature"] == 38.0
    assert isinstance(result[0]["temperature"], float)
    assert result[0]["city"] == "Springfield"


def test_convert_numeric_columns_invalid_value():
    records = [
        {"temperature": "unknown"}
    ]

    with pytest.raises(ValueError, match="Invalid numeric value"):
        convert_numeric_columns(records, ["temperature"])


def test_convert_numeric_columns_preserves_missing_values():
    records = [
        {"temperature": None},
        {"temperature": "42.5"}
    ]

    result = convert_numeric_columns(
        records,
        ["temperature"]
    )

    assert result[0]["temperature"] is None
    assert result[1]["temperature"] == 42.5


def test_convert_numeric_columns_does_not_modify_original():
    records = [
        {"temperature": "42.5"}
    ]

    convert_numeric_columns(records, ["temperature"])

    assert records[0]["temperature"] == "42.5"