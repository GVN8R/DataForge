from src.dataforge.visualization import (
    generate_trend_chart,
    generate_grouped_chart,
)
import pytest


def test_generates_trend_chart(tmp_path):
    output_path = tmp_path / "trend.png"

    trend_data = [
        {"date": "2026-01-01", "count": 2, "average": 15.0},
        {"date": "2026-01-02", "count": 1, "average": 20.0},
    ]

    result = generate_trend_chart(trend_data, output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_creates_parent_directories(tmp_path):
    output_path = tmp_path / "charts" / "trend.png"

    trend_data = [
        {"date": "2026-01-01", "count": 1, "average": 15.0},
    ]

    generate_trend_chart(trend_data, output_path)

    assert output_path.exists()


def test_rejects_empty_trend_data(tmp_path):
    with pytest.raises(ValueError, match="Trend data cannot be empty"):
        generate_trend_chart([], tmp_path / "trend.png")


def test_generates_grouped_chart(tmp_path):
    output_path = tmp_path / "grouped.png"

    grouped_data = [
        {
            "group": "Rolla",
            "count": 2,
            "total": 50,
            "average": 25,
            "minimum": 20,
            "maximum": 30,
        },
        {
            "group": "Columbia",
            "count": 2,
            "total": 90,
            "average": 45,
            "minimum": 40,
            "maximum": 50,
        },
    ]

    result = generate_grouped_chart(grouped_data, output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_grouped_chart_creates_parent_directories(tmp_path):
    output_path = tmp_path / "charts" / "grouped.png"

    grouped_data = [
        {"group": "Rolla", "average": 25}
    ]

    generate_grouped_chart(grouped_data, output_path)

    assert output_path.exists()


def test_grouped_chart_rejects_empty_data(tmp_path):
    with pytest.raises(ValueError, match="Grouped data cannot be empty"):
        generate_grouped_chart([], tmp_path / "grouped.png")
