from src.dataforge.analytics import (
    calculate_grouped_statistics,
    calculate_time_trend,
    detect_outliers,
    calculate_correlation,
    analyze_dataset,
)
import pytest
import math


def test_calculates_grouped_statistics():
    records = [
        {"city": "Rolla", "temperature": 20},
        {"city": "Rolla", "temperature": 30},
        {"city": "Columbia", "temperature": 40},
        {"city": "Columbia", "temperature": 50},
    ]

    result = calculate_grouped_statistics(
        records, "city", "temperature"
    )

    assert result == [
        {
            "group": "Columbia",
            "count": 2,
            "average": 45,
        },
        {
            "group": "Rolla",
            "count": 2,
            "average": 25,
        },
    ]


def test_ignores_missing_values():
    records = [
        {"city": "Rolla", "temperature": 20},
        {"city": "Rolla", "temperature": None},
        {"city": None, "temperature": 30},
        {"city": "Rolla", "temperature": 40},
    ]

    result = calculate_grouped_statistics(
        records, "city", "temperature"
    )

    assert len(result) == 1
    assert result[0]["count"] == 2
    assert result[0]["average"] == 30


def test_ignores_non_numeric_values():
    records = [
        {"city": "Rolla", "temperature": 20},
        {"city": "Rolla", "temperature": "invalid"},
        {"city": "Rolla", "temperature": 40},
    ]

    result = calculate_grouped_statistics(
        records, "city", "temperature"
    )

    assert result[0]["count"] == 2
    assert result[0]["average"] == 30


def test_returns_empty_list_for_empty_dataset():
    result = calculate_grouped_statistics(
        [], "city", "temperature"
    )

    assert result == []


def test_raises_error_for_missing_columns():
    records = [
        {"city": "Rolla", "rainfall": 10}
    ]

    with pytest.raises(ValueError, match="Missing required columns"):
        calculate_grouped_statistics(
            records, "city", "temperature"
        )


def test_time_trend_returns_chronological_order():
    records = [
        {"date": "2023-01-01", "value": 10},
        {"date": "2023-01-03", "value": 30},
        {"date": "2023-01-02", "value": 20},
    ]

    result = calculate_time_trend(
        records, "date", "value"
    )

    assert result == [
        {
            "date": "2023-01-01",
            "count": 1,
            "average": 10,
        },
        {
            "date": "2023-01-02",
            "count": 1,
            "average": 20,
        },
        {
            "date": "2023-01-03",
            "count": 1,
            "average": 30,
        },
    ]


def test_time_trend_calculates_average():
    records = [
        {"date": "2023-01-01", "value": 10},
        {"date": "2023-01-01", "value": 20},
        {"date": "2023-01-02", "value": 30},
    ]

    result = calculate_time_trend(
        records, "date", "value"
    )

    assert result == [
        {
            "date": "2023-01-01",
            "count": 2,
            "average": 15,
        },
        {
            "date": "2023-01-02",
            "count": 1,
            "average": 30,
        },
    ]


def test_time_trend_ignores_missing_values():
    records = [
        {"date": "2023-01-01", "value": 10},
        {"date": "2023-01-01", "value": None},
        {"date": None, "value": 20},
        {"date": "2023-01-02", "value": 30},
    ]

    result = calculate_time_trend(
        records, "date", "value"
    )

    assert len(result) == 2
    assert result[0]["count"] == 1
    assert result[0]["average"] == 10
    assert result[1]["count"] == 1
    assert result[1]["average"] == 30


def test_time_trend_ignores_non_numeric_values():
    records = [
        {"date": "2023-01-01", "value": 10},
        {"date": "2023-01-01", "value": "invalid"},
        {"date": "2023-01-02", "value": 30},
    ]

    result = calculate_time_trend(
        records, "date", "value"
    )

    assert result[0]["count"] == 1
    assert result[0]["average"] == 10
    assert result[1]["count"] == 1
    assert result[1]["average"] == 30


def test_time_trend_returns_empty_list_for_empty_dataset():
    result = calculate_time_trend(
        [], "date", "value"
    )

    assert result == []


def test_time_trend_raises_error_for_missing_columns():
    records = [
        {"date": "2023-01-01", "rainfall": 10}
    ]

    with pytest.raises(ValueError, match="Missing required columns"):
        calculate_time_trend(records, "date", "temperature")


def test_outliers_detects_high_values():
    records = [
        {"value": 10},
        {"value": 12},
        {"value": 14},
        {"value": 100},  # Outlier
    ]

    result = detect_outliers(records, "value")

    assert result == [100]


def test_outliers_detects_low_values():
    records = [
        {"value": 10},
        {"value": 12},
        {"value": 14},
        {"value": -50},  # Outlier
    ]

    result = detect_outliers(records, "value")

    assert result == [-50]


def test_outliers_no_false_positives():
    records = [
        {"value": 10},
        {"value": 12},
        {"value": 14},
        {"value": 15},
    ]

    result = detect_outliers(records, "value")

    assert result == []


def test_outliers_ignores_non_numeric_values():
    records = [
        {"value": 10},
        {"value": "invalid"},
        {"value": 14},
        {"value": None},
    ]

    result = detect_outliers(records, "value")

    assert result == []


def test_outliers_returns_empty_list_for_dataset_smaller_than_four():
    records = [
        {"value": 10},
        {"value": 12},
        {"value": 14},
    ]

    result = detect_outliers(records, "value")

    assert result == []


def test_correlation_with_perfect_positive_correlation():
    records = [
        {"x": 1, "y": 2},
        {"x": 2, "y": 4},
        {"x": 3, "y": 6},
        {"x": 4, "y": 8},
    ]

    result = calculate_correlation(records, "x", "y")

    assert math.isclose(result, 1.0, rel_tol=1e-9)


def test_correlation_with_perfect_negative_correlation():
    records = [
        {"x": 1, "y": 8},
        {"x": 2, "y": 6},
        {"x": 3, "y": 4},
        {"x": 4, "y": 2},
    ]

    result = calculate_correlation(records, "x", "y")

    assert math.isclose(result, -1.0, rel_tol=1e-9)


def test_correlation_with_no_correlation():
    records = [
        {"x": 1, "y": 1},
        {"x": 1, "y": 3},
        {"x": 3, "y": 1},
        {"x": 3, "y": 3},
    ]

    result = calculate_correlation(records, "x", "y")

    assert math.isclose(result, 0, rel_tol=1e-9)


def test_correlation_ignores_non_numeric_values():
    records = [
        {"x": 1, "y": 2},
        {"x": 2, "y": "invalid"},
        {"x": 3, "y": 6},
        {"x": None, "y": 8},
    ]

    result = calculate_correlation(records, "x", "y")

    assert math.isclose(result, 1.0, rel_tol=1e-9)


def test_correlation_returns_none_for_insufficient_data():
    records = [
        {"x": 1, "y": 2},
    ]

    result = calculate_correlation(records, "x", "y")

    assert result is None


def test_correlation_raises_error_for_missing_columns():
    records = [
        {"x": 1, "z": 2}
    ]

    with pytest.raises(ValueError, match="Missing required columns"):
        calculate_correlation(records, "x", "y")


def test_analyze_includes_all_analytics():
    records = [
        {"city": "Rolla", "temperature": 20, "date": "2023-01-01", "value": 10},
        {"city": "Rolla", "temperature": 30, "date": "2023-01-02", "value": 20},
        {"city": "Columbia", "temperature": 40, "date": "2023-01-01", "value": 30},
        {"city": "Columbia", "temperature": 50, "date": "2023-01-02", "value": 40},
    ]

    result = analyze_dataset(
        records,
        group_column="city",
        numeric_column="temperature",
        date_column="date",
        correlation_column="value",
    )

    assert result["grouped_statistics"] == [
        {
            "group": "Columbia",
            "count": 2,
            "average": 45,
        },
        {
            "group": "Rolla",
            "count": 2,
            "average": 25,
        },
    ]
    assert result["time_trend"] == [
        {
            "date": "2023-01-01",
            "count": 2,
            "average": 30,
        },
        {
            "date": "2023-01-02",
            "count": 2,
            "average": 40,
        },
    ]
    assert result["outliers"] == []
    assert result["correlation"] is not None


def test_analyze_returns_none_for_missing_columns():
    records = [
        {"city": "Rolla", "temperature": 20},
        {"city": "Columbia", "temperature": 40},
    ]

    result = analyze_dataset(
        records,
        group_column="city",
        numeric_column="temperature",
        date_column=None,  # Missing column
        correlation_column=None,  # Missing column
    )

    assert result["grouped_statistics"] is not None
    assert result["time_trend"] is None
    assert result["outliers"] is not None
    assert result["correlation"] is None


def test_analyze_returns_empty_report_for_empty_dataset():
    result = analyze_dataset(
        [],
        group_column="city",
        numeric_column="temperature",
        date_column="date",
        correlation_column="value",
    )

    assert result == {
        "record_count": 0,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }