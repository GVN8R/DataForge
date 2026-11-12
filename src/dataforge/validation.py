def find_missing_values(records):
    issues = []

    for row_number, record in enumerate(records, start=1):
        for column, value in record.items():
            if value is None or value.strip() == "":
                issues.append({
                    "row": row_number,
                    "column": column,
                    "issue": "Missing value"
                })
    
    return issues


def find_duplicates(records):
    seen = set()
    duplicates = []

    for row_number, record in enumerate(records, start=1):
        record_key = tuple(sorted(record.items()))

        if record_key in seen:
            duplicates.append({
                "row": row_number,
                "issue": "Duplicate record"
            })
        else:
            seen.add(record_key)
    
    return duplicates


def validate_records(records):
    return {
        "missing_values": find_missing_values(records),
        "duplicates": find_duplicates(records)
    }