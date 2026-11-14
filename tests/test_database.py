from src.dataforge.database import (
    connect_database,
    initialize_database
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