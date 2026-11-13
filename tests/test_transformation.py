import pytest
from src.dataforge.transformation import (
    normalize_column_names,
    normalize_text_values
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