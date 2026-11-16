from src.dataforge.reporting import (
    generate_html_report,
    generate_markdown_report,
    save_markdown_report,
    save_html_report,
    generate_html_report_with_charts,
)
import pytest


def test_report_includes_title():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    report = generate_markdown_report(analysis_report, title="Custom Report Title")
    assert "# Custom Report Title" in report


def test_report_includes_grouped_statistics():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": [
            {"group": "A", "count": 50, "average": 10.5},
            {"group": "B", "count": 50, "average": 20.5}
        ],
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    report = generate_markdown_report(analysis_report)
    assert "## Grouped Statistics" in report
    assert "| A | 50 | 10.50 |" in report
    assert "| B | 50 | 20.50 |" in report


def test_report_includes_time_trend():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": [
            {"date": "2023-01-01", "count": 10, "average": 5.0},
            {"date": "2023-01-02", "count": 20, "average": 15.0}
        ],
        "outliers": None,
        "correlation": None
    }
    report = generate_markdown_report(analysis_report)
    assert "## Time Trend" in report
    assert "| 2023-01-01 | 10 | 5.00 |" in report
    assert "| 2023-01-02 | 20 | 15.00 |" in report


def test_report_displays_outliers():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": [
            {"id": 1, "value": 100},
            {"id": 2, "value": 200}
        ],
        "correlation": None
    }
    report = generate_markdown_report(analysis_report)
    assert "## Outliers" in report
    assert "| 100 |" in report
    assert "| 200 |" in report


def test_report_displays_correlation():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": 0.85
    }
    report = generate_markdown_report(analysis_report)
    assert "## Correlation" in report
    assert "Correlation coefficient: 0.8500" in report


def test_report_handles_empty_analysis():
    analysis_report = {
        "record_count": 0,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    report = generate_markdown_report(analysis_report)
    assert "No data available for analysis." in report


def test_report_returns_full_report():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": [
            {"group": "A", "count": 50, "average": 10.5},
            {"group": "B", "count": 50, "average": 20.5}
        ],
        "time_trend": [
            {"date": "2023-01-01", "count": 10, "average": 5.0},
            {"date": "2023-01-02", "count": 20, "average": 15.0}
        ],
        "outliers": [
            {"id": 1, "value": 100},
            {"id": 2, "value": 200}
        ],
        "correlation": 0.85
    }
    report = generate_markdown_report(analysis_report)
    assert "# DataForge Analysis Report" in report
    assert "## Grouped Statistics" in report
    assert "| A | 50 | 10.50 |" in report
    assert "| B | 50 | 20.50 |" in report
    assert "## Time Trend" in report
    assert "| 2023-01-01 | 10 | 5.00 |" in report
    assert "| 2023-01-02 | 20 | 15.00 |" in report
    assert "## Outliers" in report
    assert "| 100 |" in report
    assert "| 200 |" in report
    assert "## Correlation" in report
    assert "Correlation coefficient: 0.8500" in report


def test_saves_markdown_report(tmp_path):
    output_path = tmp_path / "report.md"

    result = save_markdown_report(
        "# DataForge Report",
        output_path
    )

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == "# DataForge Report"


def test_creates_parent_directories(tmp_path):
    output_path = tmp_path / "reports" / "weekly" / "report.md"

    save_markdown_report("# Report", output_path)

    assert output_path.exists()


def test_rejects_non_string_content(tmp_path):
    with pytest.raises(TypeError):
        save_markdown_report(None, tmp_path / "report.md")


def test_rejects_empty_content(tmp_path):
    with pytest.raises(ValueError):
        save_markdown_report("   ", tmp_path / "report.md")


def test_overwrites_existing_report(tmp_path):
    output_path = tmp_path / "report.md"
    output_path.write_text("Old report", encoding="utf-8")

    save_markdown_report("New report", output_path)

    assert output_path.read_text(encoding="utf-8") == "New report"


def test_html_contains_html_structure():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report, title="HTML Report")
    assert "<html>" in html_report
    assert "<head>" in html_report
    assert "<body>" in html_report
    assert "<h1>HTML Report</h1>" in html_report


def test_html_includes_title():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report, title="HTML Report")
    assert "<h1>HTML Report</h1>" in html_report


def test_html_markdown_headings_converted_to_html():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report)
    assert "<h1>DataForge Analysis Report</h1>" in html_report



def test_saves_html_report(tmp_path):
    output_path = tmp_path / "report.html"

    result = save_html_report(
        "<html><body>Report</body></html>",
        output_path
    )

    assert result == output_path
    assert output_path.read_text(encoding="utf-8") == (
        "<html><body>Report</body></html>"
    )


def test_creates_parent_directories_for_html(tmp_path):
    output_path = tmp_path / "reports" / "html" / "report.html"

    save_html_report("<h1>Report</h1>", output_path)

    assert output_path.exists()


def test_rejects_non_string_html_content(tmp_path):
    with pytest.raises(TypeError):
        save_html_report(None, tmp_path / "report.html")


def test_rejects_empty_html_content(tmp_path):
    with pytest.raises(ValueError):
        save_html_report("   ", tmp_path / "report.html")


def test_overwrites_existing_html_report(tmp_path):
    output_path = tmp_path / "report.html"
    output_path.write_text("Old report", encoding="utf-8")

    save_html_report("<h1>New report</h1>", output_path)

    assert output_path.read_text(encoding="utf-8") == (
        "<h1>New report</h1>"
    )


def test_html_markdown_table_converted_to_html_table():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": [
            {"group": "A", "count": 50, "average": 10.5},
            {"group": "B", "count": 50, "average": 20.5}
        ],
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report)
    assert "<table>" in html_report
    assert "<th>Group</th>" in html_report
    assert "<td>A</td>" in html_report
    assert "<td>50</td>" in html_report
    assert "<td>10.50</td>" in html_report


def test_html_table_headers_become_th_elements():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": [
            {"group": "A", "count": 50, "average": 10.5}
        ],
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report)
    assert "<th>Group</th>" in html_report
    assert "<th>Count</th>" in html_report
    assert "<th>Average</th>" in html_report


def test_html_table_values_become_td_elements():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": [
            {"group": "A", "count": 50, "average": 10.5}
        ],
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report(analysis_report)
    assert "<td>A</td>" in html_report
    assert "<td>50</td>" in html_report
    assert "<td>10.50</td>" in html_report


def test_chart_html_includes_time_trend_chart():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": [
            {"date": "2023-01-01", "count": 10, "average": 5.0},
            {"date": "2023-01-02", "count": 20, "average": 15.0}
        ],
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report_with_charts(analysis_report)
    assert "<img src=" in html_report


def test_chart_html_ignores_missing_chart_file():
    analysis_report = {
        "record_count": 100,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }
    html_report = generate_html_report_with_charts(analysis_report)
    assert "<canvas id=\"timeTrendChart\"></canvas>" not in html_report
    assert "<canvas id=\"groupedStatisticsChart\"></canvas>" not in html_report