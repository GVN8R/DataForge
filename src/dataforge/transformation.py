from src.dataforge.validation import generate_full_quality_report
from datetime import datetime

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
    converted_records = []

    for record in records:
        converted_record = record.copy()

        for column in columns:
            value = converted_record.get(column)

            if value is None:
                continue

            try:
                converted_record[column] = float(value)
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid numeric value in column "
                    f"'{column}': {value}"
                )

        converted_records.append(converted_record)

    return converted_records


def normalize_date_columns(records, columns, date_format=None):
    normalized_records = []

    for record in records:
        normalized_record = record.copy()

        for column in columns:
            value = normalized_record.get(column)

            if value is None:
                continue

            try:
                if date_format:
                    parsed_date = datetime.strptime(
                        value,
                        date_format
                    )
                else:
                    parsed_date = datetime.fromisoformat(value)

                normalized_record[column] = parsed_date.date().isoformat()

            except(ValueError, TypeError):
                raise ValueError(
                    f"Invalid date in column '{column}': {value}"
                )

        normalized_records.append(normalized_record)

    return normalized_records


def transform_records(records, rules):
    transformed = normalize_column_names(records)

    transformed = normalize_text_values(transformed)

    transformed = normalize_missing_values(
        transformed,
        rules.get("missing_markers")
    )

    transformed = convert_numeric_columns(
        transformed,
        rules.get("numeric_columns", [])
    )

    transformed = normalize_date_columns(
        transformed,
        rules.get("date_columns", []),
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