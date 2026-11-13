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