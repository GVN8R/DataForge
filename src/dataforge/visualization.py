import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib


matplotlib.use("Agg")


def generate_trend_chart(trend_data, output_path):
    """Generate a line chart from time-trend analysis results."""
    if not trend_data:
        raise ValueError("Trend data cannot be empty.")

    dates = [item["date"] for item in trend_data]
    averages = [item["average"] for item in trend_data]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 5))

    try:
        axis.plot(dates, averages, marker="o")
        axis.set_title("Data Trend Over Time")
        axis.set_xlabel("Date")
        axis.set_ylabel("Average Value")
        axis.tick_params(axis="x", rotation=45)

        figure.tight_layout()
        figure.savefig(output_path, dpi=150)
    finally:
        plt.close(figure)

    return output_path


def generate_grouped_chart(grouped_data, output_path):
    """Generate a bar chart from grouped numerical statistics."""
    if not grouped_data:
        raise ValueError("Grouped data cannot be empty.")

    groups = [item["group"] for item in grouped_data]
    averages = [item["average"] for item in grouped_data]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 5))

    try:
        axis.bar(groups, averages)
        axis.set_title("Average Value by Group")
        axis.set_xlabel("Group")
        axis.set_ylabel("Average Value")
        axis.tick_params(axis="x", rotation=45)

        figure.tight_layout()
        figure.savefig(output_path, dpi=150)
    finally:
        plt.close(figure)

    return output_path

