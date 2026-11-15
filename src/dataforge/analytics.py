import math


def calculate_grouped_statistics(records, group_column, numeric_column):
    """Calculate numerical statistics for each category in a dataset."""
    if not records:
        return []

    required_columns = {group_column, numeric_column}
    missing_columns = required_columns - records[0].keys()

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    groups = {}

    for record in records:
        group_value = record.get(group_column)
        numeric_value = record.get(numeric_column)

        # Ignore records with missing category or numeric values.
        if group_value is None or str(group_value).strip() == "":
            continue

        if (
            numeric_value is None
            or isinstance(numeric_value, bool)
            or not isinstance(numeric_value, (int, float))
        ):
            continue

        groups.setdefault(group_value, []).append(numeric_value)

    results = []

    for group_value, values in groups.items():
        results.append({
            "group": group_value,
            "count": len(values),
            "average": sum(values) / len(values),
        })

    return sorted(results, key=lambda result: str(result["group"]))


def calculate_time_trend(records, date_column, numeric_column):
    """Calculate numerical statistics for each date in a dataset."""
    if not records:
        return []

    required_columns = {date_column, numeric_column}
    missing_columns = required_columns - records[0].keys()

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    trends = {}

    for record in records:
        date_value = record.get(date_column)
        numeric_value = record.get(numeric_column)

        # Ignore records with missing date or numeric values.
        if date_value is None or str(date_value).strip() == "":
            continue

        if (
            numeric_value is None
            or isinstance(numeric_value, bool)
            or not isinstance(numeric_value, (int, float))
        ):
            continue

        trends.setdefault(date_value, []).append(numeric_value)

    results = []

    for date_value, values in trends.items():
        results.append({
            "date": date_value,
            "count": len(values),
            "average": sum(values) / len(values),
        })

    return sorted(results, key=lambda result: str(result["date"]))


def detect_outliers(records, numeric_column):
    """Identify numerical outliers using the IQR method."""
    if not records:
        return []

    if numeric_column not in records[0]:
        raise ValueError(f"Missing required column: {numeric_column}")

    values = [
        record[numeric_column]
        for record in records
        if isinstance(record.get(numeric_column), (int, float))
        and not isinstance(record.get(numeric_column), bool)
    ]

    if len(values) < 4:
        return []

    sorted_values = sorted(values)

    def percentile(data, fraction):
        position = (len(data) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(data) - 1)
        weight = position - lower

        return (
            data[lower] * (1 - weight)
            + data[upper] * weight
        )

    q1 = percentile(sorted_values, 0.25)
    q3 = percentile(sorted_values, 0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return [
        record[numeric_column]
        for record in records
        if isinstance(record.get(numeric_column), (int, float))
        and not isinstance(record.get(numeric_column), bool)
        and (
            record[numeric_column] < lower_bound
            or record[numeric_column] > upper_bound
        )
    ]


def calculate_correlation(records, first_column, second_column):
    """Calculate Pearson correlation between two numeric columns."""
    if not records:
        return None

    required_columns = {first_column, second_column}
    missing_columns = required_columns - records[0].keys()

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    pairs = []

    for record in records:
        x = record.get(first_column)
        y = record.get(second_column)

        if (
            isinstance(x, (int, float))
            and not isinstance(x, bool)
            and isinstance(y, (int, float))
            and not isinstance(y, bool)
            and math.isfinite(x)
            and math.isfinite(y)
        ):
            pairs.append((x, y))

    if len(pairs) < 2:
        return None

    x_values = [pair[0] for pair in pairs]
    y_values = [pair[1] for pair in pairs]

    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in pairs
    )

    x_squared = sum((x - x_mean) ** 2 for x in x_values)
    y_squared = sum((y - y_mean) ** 2 for y in y_values)

    denominator = math.sqrt(x_squared * y_squared)

    if denominator == 0:
        return None

    return numerator / denominator



def analyze_dataset(
    records,
    group_column=None,
    numeric_column=None,
    date_column=None,
    correlation_column=None
):
    """Run selected analytics on a dataset."""
    report = {
        "record_count": len(records),
        "grouped_statistics": None,
        "time_trend": None,
        "outliers": None,
        "correlation": None
    }

    if not records:
        return report

    if group_column and numeric_column:
        report["grouped_statistics"] = calculate_grouped_statistics(
            records, group_column, numeric_column
        )

    if date_column and numeric_column:
        report["time_trend"] = calculate_time_trend(
            records, date_column, numeric_column
        )

    if numeric_column:
        report["outliers"] = detect_outliers(
            records, numeric_column
        )

    if numeric_column and correlation_column:
        report["correlation"] = calculate_correlation(
            records, numeric_column, correlation_column
        )

    return report
