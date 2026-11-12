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

def generate_quality_report(records):
    results = validate_records(records)

    missing_count = len(results["missing_values"])
    duplicate_count = len(results["duplicates"])

    return {
        "total_records": len(records),
        "missing_values": missing_count,
        "duplicate_records": duplicate_count,
        "total_issues": missing_count + duplicate_count,
        "passed": missing_count == 0 and duplicate_count == 0
    }


def find_invalid_numbers(records, columns):
    issues = []

    for row_number, record in enumerate(records, start=1):
        for column in columns:
            value = record.get(column)

            if value is None or value.strip() == "":
                continue
            
            try:
                float(value)
            except ValueError:
                issues.append({
                    "row": row_number,
                    "column": column,
                    "value": value,
                    "issue": "Invalid numeric value"
                })
    
    return issues


def validate_with_rules(records, rules):
    results = {}

    results["missing_columns"] = find_missing_columns(
        records,
        rules.get("required_columns", [])
    )

    results["missing_values"] = find_missing_values(records)

    results["duplicates"] = find_duplicates(records)

    results["invalid_numbers"] = find_invalid_numbers(
        records,
        rules.get("numeric_columns", [])
    )

    results["duplicate_values"] = find_duplicate_values(
        records,
        rules.get("unique_columns", [])
    )

    return results


def find_missing_columns(records, required_columns):
    if not records:
        return [
            {
                "column": column,
                "issue": "Required column missing"
            }
            for column in required_columns
        ]
    
    available_columns = set(records[0].keys())

    issues = []

    for column in required_columns:
        if column not in available_columns:
            issues.append({
                "column": column,
                "issue": "Required column missing"
            })
    
    return issues


def find_duplicate_values(records, columns):
    issues = []

    for column in columns:
        seen = set()

        for row_number, record in enumerate(records, start=1):
            value = record.get(column)

            if value is None or value.strip() == "":
                continue
            
            if value in seen:
                issues.append({
                    "row": row_number,
                    "column": column,
                    "value": value,
                    "issue": "Duplicate column value"
                })
            else:
                seen.add(value)
    
    return issues