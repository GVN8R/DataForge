from src.dataforge.database import (
    connect_database,
    initialize_database,
    save_dataset,
    get_dataset_records,
    list_datasets,
    get_dataset
)
import sqlite3
import pytest


def initialize_database_creates_file(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)

    assert db_path.exists()


def test_initialize_database_creates_tables(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)

    connection = connect_database(db_path)

    try:
        tables = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """).fetchall()

        table_names = {table[0] for table in tables}

        assert "datasets" in table_names
        assert "records" in table_names
    finally:
        connection.close()


def test_initialize_database_is_repeatable(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)
    initialize_database(db_path)

    connection = connect_database(db_path)

    try:
        tables = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """).fetchall()

        table_names = {table[0] for table in tables}

        assert "datasets" in table_names
        assert "records" in table_names
    finally:
        connection.close()


def test_database_enforces_foreign_keys(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)
    connection = connect_database(db_path)

    try:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("""
                INSERT INTO records (
                    dataset_id,
                    row_number,
                    data_json
                )
                VALUES (999, 1, '{}')
            """)
    finally:
        connection.close()


def test_save_dataset_returns_id(tmp_path):
    db_path = tmp_path / "dataforge.db"

    records = [
        {"city": "Rolla", "temperature": 72.0}
    ]

    dataset_id = save_dataset(
        db_path,
        "weather.csv",
        records
    )

    assert isinstance(dataset_id, int)
    assert dataset_id > 0


def test_save_dataset_persists_dataset_metadata(tmp_path):
    db_path = tmp_path / "dataforge.db"

    records = [
        {"city": "Rolla"},
        {"city": "Columbia"}
    ]

    dataset_id = save_dataset(
        db_path,
        "weather.csv",
        records
    )

    connection = connect_database(db_path)

    try:
        dataset = connection.execute(
            """
            SELECT source_file, record_count
            FROM datasets
            WHERE id = ?
            """,
            (dataset_id,)
        ).fetchone()

        assert dataset == ("weather.csv", 2)
    finally:
        connection.close()


def test_get_dataset_records_returns_saved_records(tmp_path):
    db_path = tmp_path / "dataforge.db"

    records = [
        {"city": "Rolla", "temperature": 72.0},
        {"city": "Columbia", "temperature": 75.0}
    ]

    dataset_id = save_dataset(
        db_path,
        "weather.csv",
        records
    )

    retrieved = get_dataset_records(db_path, dataset_id)

    assert retrieved == records


def test_save_empty_dataset(tmp_path):
    db_path = tmp_path / "dataforge.db"

    dataset_id = save_dataset(
        db_path,
        "empty.csv",
        []
    )

    assert get_dataset_records(db_path, dataset_id) == []


def test_list_datasets_returns_all_datasets(tmp_path):
    db_path = tmp_path / "dataforge.db"

    first_id = save_dataset(
        db_path,
        "weather.csv",
        [{"city": "Rolla"}]
    )

    second_id = save_dataset(
        db_path,
        "population.csv",
        [{"city": "Columbia"}, {"city": "Rolla"}]
    )

    datasets = list_datasets(db_path)

    assert len(datasets) == 2
    assert datasets[0]["id"] == second_id
    assert datasets[1]["id"] == first_id


def test_list_datasets_returns_empty_list(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)

    assert list_datasets(db_path) == []


def test_get_dataset_returns_correct_metadata(tmp_path):
    db_path = tmp_path / "dataforge.db"

    dataset_id = save_dataset(
        db_path,
        "weather.csv",
        [{"city": "Rolla"}]
    )

    dataset = get_dataset(db_path, dataset_id)

    assert dataset["id"] == dataset_id
    assert dataset["source_file"] == "weather.csv"
    assert dataset["record_count"] == 1
    assert dataset["imported_at"] is not None


def test_get_dataset_returns_none_for_unknown_id(tmp_path):
    db_path = tmp_path / "dataforge.db"

    initialize_database(db_path)

    assert get_dataset(db_path, 999) is None