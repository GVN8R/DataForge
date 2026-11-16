from src.dataforge.transformation import process_records
from src.dataforge.ingestion import read_csv
from src.dataforge.export import write_csv
from pathlib import Path


def run_pipeline(
        input_path,
        output_path,
        validation_rules,
        transformation_rules
):
    if not isinstance(validation_rules, dict):
        raise TypeError("validation_rules must be a dictionary.")

    if not isinstance(transformation_rules, dict):
        raise TypeError("transformation_rules must be a dictionary.")

    if not str(input_path).strip():
        raise ValueError("input_path cannot be empty.")

    if not str(output_path).strip():
        raise ValueError("output_path cannot be empty.")

    raw_records = read_csv(input_path)

    result = process_records(
        raw_records,
        validation_rules,
        transformation_rules
    )

    transformed_records = result["transformed_records"]

    write_csv(transformed_records, output_path)

    return {
        "validation_report": result["validation_report"],
        "records_processed": len(transformed_records),
        "output_path": str(output_path)
    }