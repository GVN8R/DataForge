from src.dataforge.visualization import (
    generate_trend_chart,
    generate_grouped_chart,
)
from pathlib import Path
import html


def generate_markdown_report(analysis_report, title="DataForge Analysis Report"):
    """Generate a Markdown report from dataset analysis results."""
    report_lines = [f"# {title}\n"]

    if analysis_report.get("grouped_statistics"):
        report_lines.append("## Grouped Statistics")
        report_lines.append("| Group   | Count | Average |")
        report_lines.append("|---------|-------|---------|")
        for group in analysis_report["grouped_statistics"]:
            report_lines.append(f"| {group['group']} | {group['count']} | {group['average']:.2f} |")


    if analysis_report.get("time_trend"):
        report_lines.append("## Time Trend")
        report_lines.append("| Date    | Count | Average |")
        report_lines.append("|---------|-------|---------|")
        for trend in analysis_report["time_trend"]:
            report_lines.append(f"| {trend['date']} | {trend['count']} | {trend['average']:.2f} |")

    if analysis_report.get("outliers"):
        report_lines.append("## Outliers")
        report_lines.append("| Value |")
        report_lines.append("|-------|")
        for outlier in analysis_report["outliers"]:
            report_lines.append(f"| {outlier['value']} |")

    if analysis_report.get("correlation") is not None:
        report_lines.append("## Correlation")
        report_lines.append(f"Correlation coefficient: {analysis_report['correlation']:.4f}")

    if analysis_report == {
        "record_count": 0,
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }:
        report_lines.append("No data available for analysis.")

    return "\n".join(report_lines)


def save_markdown_report(report_content, output_path):
    """Save a Markdown report to a file."""
    if not isinstance(report_content, str):
        raise TypeError("Report content must be a string.")

    if not report_content.strip():
        raise ValueError("Report content cannot be empty.")

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_content, encoding="utf-8")

    return output_path


def generate_html_report(analysis_report, title="DataForge Analysis Report"):
    """Generate a standalone HTML report from analysis results."""
    markdown = generate_markdown_report(analysis_report, title)

    def convert_table(lines):
        rows = []

        for line in lines:
            cells = [
                cell.strip()
                for cell in line.strip().strip("|").split("|")
            ]

            if all(
                set(cell) <= {"-", ":"}
                for cell in cells
            ):
                continue

            rows.append(cells)

        if not rows:
            return ""

        header = "".join(
            f"<th>{html.escape(cell)}</th>"
            for cell in rows[0]
        )

        body = "".join(
            "<tr>" + "".join(
                f"<td>{html.escape(cell)}</td>"
                for cell in row
            ) + "</tr>"
            for row in rows[1:]
        )

        return (
            "<table><thead><tr>"
            + header
            + "</tr></thead><tbody>"
            + body
            + "</tbody></table>"
        )

    html_lines = []
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.strip().startswith("|"):
            table_lines = []

            while (
                index < len(lines)
                and lines[index].strip().startswith("|")
            ):
                table_lines.append(lines[index])
                index += 1

            html_lines.append(convert_table(table_lines))
            continue

        escaped_line = html.escape(line)

        if line.startswith("# "):
            html_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.strip():
            html_lines.append(f"<p>{escaped_line}</p>")

        index += 1

    body = "\n".join(html_lines)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + html.escape(title) + """</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1000px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #222;
            background: #f7f9fc;
        }}
        h1, h2 {{
            color: #174a72;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background: #174a72;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f0f4f8;
        }}
    </style>
</head>
<body>
""" + body + """
</body>
</html>"""


def save_html_report(report_content, output_path):
    """Save an HTML report to a file."""
    if not isinstance(report_content, str):
        raise TypeError("Report content must be a string.")

    if not report_content.strip():
        raise ValueError("Report content cannot be empty.")

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_content, encoding="utf-8")

    return output_path


def generate_html_report_with_charts(
    analysis_report,
    trend_chart_path=None,
    grouped_chart_path=None,
    title="DataForge Analysis Report"
):
    """Generate an HTML report with automatically generated charts."""

    html_content = generate_html_report(analysis_report, title)
    chart_sections = []

    # Automatically generate a trend chart when trend data exists.
    trend_data = analysis_report.get("time_trend")

    if trend_data:
        if trend_chart_path is None:
            trend_chart_path = Path("reports/charts/trend.png")

        generate_trend_chart(trend_data, trend_chart_path)

        chart_sections.append(
            '<section><h2>Trend Chart</h2>'
            f'<img src="{html.escape(str(trend_chart_path))}" '
            'alt="Trend chart" style="max-width:100%;"></section>'
        )

    # Automatically generate a grouped statistics chart.
    grouped_data = analysis_report.get("grouped_statistics")

    if grouped_data:
        if grouped_chart_path is None:
            grouped_chart_path = Path("reports/charts/grouped.png")

        generate_grouped_chart(grouped_data, grouped_chart_path)

        chart_sections.append(
            '<section><h2>Grouped Statistics Chart</h2>'
            f'<img src="{html.escape(str(grouped_chart_path))}" '
            'alt="Grouped statistics chart" style="max-width:100%;"></section>'
        )

    if chart_sections:
        html_content = html_content.replace(
            "</body>",
            "\n".join(chart_sections) + "\n</body>"
        )

    return html_content
