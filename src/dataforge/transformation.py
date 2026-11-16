from src.dataforge.validation import generate_full_quality_report
from datetime import datetime
import math

def normalize_column_names(records):
    if not records:
        return []
    
    normalized_records = []

    for record in records:
        normalized_record = {}

        for column, value in record.items():
            normalized_column = column.strip().lower()

            if normalized_column in normalized_record:
                raise ValueError(
                    f"Column name collision after normalization: "
                    f"{normalized_column}"
                )
            
            normalized_record[normalized_column] = value
        
        normalized_records.append(normalized_record)
    
    return normalized_records


def normalize_text_values(records):
    normalized_records = []

    for record in records:
        normalized_record = {}

        for column, value in record.items():
            if isinstance(value, str):
                normalized_record[column] = value.strip()
            else:
                normalized_record[column] = value
        
        normalized_records.append(normalized_record)
    
    return normalized_records


def normalize_missing_values(records, missing_markers=None):
    if missing_markers is None:
        missing_markers = {"", "n/a", "na", "unknown", "null"}

    normalized_markers = {
        marker.strip().lower()
        for marker in missing_markers
    }

    normalized_records = []

    for record in records:
        normalized_record = {}

        for column, value in record.items():
            if isinstance(value, str):
                cleaned_value = value.strip()

                if cleaned_value.lower() in normalized_markers:
                    normalized_record[column] = None
                else:
                    normalized_record[column] = cleaned_value
            else:
                normalized_record[column] = value

        normalized_records.append(normalized_record)

    return normalized_records


def convert_numeric_columns(records, columns):
    """Convert selected columns to finite floating-point numbers."""
    converted_records = []

    for row_number, record in enumerate(records, start=1):
        converted_record = record.copy()

        for column in columns:
            if column not in converted_record:
                raise ValueError(
                    f"Missing column '{column}' in row {row_number}."
                )

            value = converted_record[column]

            if value is None:
                continue

            try:
                numeric_value = float(value)
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid numeric value in column '{column}', "
                    f"row {row_number}: {value}"
                ) from error

            if not math.isfinite(numeric_value):
                raise ValueError(
                    f"Non-finite numeric value in column '{column}', "
                    f"row {row_number}: {value}"
                )

            converted_record[column] = numeric_value

        converted_records.append(converted_record)

    return converted_records



def normalize_date_columns(records, columns, date_format=None):
    """Normalize selected date columns to YYYY-MM-DD strings."""
    normalized_records = []

    for row_number, record in enumerate(records, start=1):
        normalized_record = record.copy()

        for column in columns:
            if column not in normalized_record:
                raise ValueError(
                    f"Missing column '{column}' in row {row_number}."
                )

            value = normalized_record[column]

            if value is None:
                continue

            if not isinstance(value, str):
                raise ValueError(
                    f"Invalid date type in column '{column}', "
                    f"row {row_number}: {value}"
                )

            try:
                if date_format is not None:
                    parsed_date = datetime.strptime(value, date_format)
                else:
                    parsed_date = datetime.fromisoformat(value)

                normalized_record[column] = parsed_date.date().isoformat()

            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid date in column '{column}', "
                    f"row {row_number}: {value}"
                ) from error

        normalized_records.append(normalized_record)

    return normalized_records


def transform_records(records, rules):
    if not isinstance(rules, dict):
        raise TypeError("Transformation rules must be a dictionary.")

    numeric_columns = rules.get("numeric_columns", [])
    date_columns = rules.get("date_columns", [])

    if not isinstance(numeric_columns, (list, tuple)):
        raise TypeError("numeric_columns must be a list or tuple.")

    if not isinstance(date_columns, (list, tuple)):
        raise TypeError("date_columns must be a list or tuple.")

    if not all(isinstance(column, str) and column.strip()
               for column in numeric_columns):
        raise ValueError("numeric_columns must contain valid column names.")

    if not all(isinstance(column, str) and column.strip()
               for column in date_columns):
        raise ValueError("date_columns must contain valid column names.")

    transformed = normalize_column_names(records)

    transformed = normalize_text_values(transformed)

    transformed = normalize_missing_values(
        transformed,
        rules.get("missing_markers")
    )

    transformed = convert_numeric_columns(
        transformed,
        numeric_columns
    )

    transformed = normalize_date_columns(
        transformed,
        date_columns,
        rules.get("date_format")
    )

    return transformed

def process_records(records, validation_rules, transformation_rules):
    validation_report = generate_full_quality_report(
        records,
        validation_rules
    )

    blocking_issues = (
        validation_report["issue_counts"]["missing columns"]
        if "missing columns" in validation_report["issue_counts"]
        else validation_report["issue_counts"]["missing_columns"]
    )

    if blocking_issues:
        raise ValueError(
            "Cannot process records: required columns are missing."
        )


    transformed_records = transform_records(
        records,
        transformation_rules
    )

    return {
        "validation_report": validation_report,
        "transformed_records": transformed_records
    }