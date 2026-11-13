from src.dataforge.pipeline import run_pipeline
import csv


def test_run_pipeline_end_to_end(tmp_path):
    input_path = tmp_path / "weather.csv"
    output_path = tmp_path / "processed" / "weather.csv"

    input_path.write_text(
        "Date,Temperature,City\n"
        "2026-01-01,72,Rolla\n"
        "2026-01-02,75,Columbia\n",
        encoding="utf-8"
    )

    validation_rules = {
        "required_columns": ["Date", "Temperature", "City"],
        "numeric_columns": ["Temperature"],
        "unique_columns": ["Date"]
    }

    transformation_rules = {
        "numeric_columns": ["temperature"],
        "date_columns": ["date"]
    }

    result = run_pipeline(
        input_path,
        output_path,
        validation_rules,
        transformation_rules
    )

    assert result["records_processed"] == 2
    assert result["validation_report"]["passed"] is True
    assert output_path.exists()

    with output_path.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        records = list(csv.DictReader(file))

    assert records[0]["date"] == "2026-01-01"
    assert records[0]["temperature"] == "72.0"
    assert records[0]["city"] == "Rolla"


def test_run_pipeline_rejects_missing_required_columns(tmp_path):
    input_path = tmp_path / "weather.csv"
    output_path = tmp_path / "processed" / "weather.csv"

    input_path.write_text(
        "Date,City\n2026-01-01,Rolla\n",
        encoding="utf-8"
    )

    validation_rules = {
        "required_columns": ["Date", "Temperature"],
        "numeric_columns": [],
        "unique_columns": []
    }

    transformation_rules = {}

    try:
        run_pipeline(
            input_path,
            output_path,
            validation_rules,
            transformation_rules
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "required columns are missing" in str(error)

    assert not output_path.exists()