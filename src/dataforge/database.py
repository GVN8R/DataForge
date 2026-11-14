from pathlib import Path
import sqlite3
import json


def connect_database(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database(db_path):
    connection = connect_database(db_path)

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                record_count INTEGER NOT NULL
                    CHECK (record_count >= 0)
            );

            CREATE TABLE IF NOT EXISTS records (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER NOT NULL,
                row_number INTEGER NOT NULL,
                data_json TEXT NOT NULL,

                FOREIGN KEY (dataset_id)
                    REFERENCES datasets(id)
                    ON DELETE CASCADE,
                
                UNIQUE (dataset_id, row_number)
            );

            CREATE INDEX IF NOT EXISTS idx_records_dataset
            ON records(dataset_id);
        """)
    finally:
        connection.close()


def save_dataset(db_path, source_file, records):
    initialize_database(db_path)
    connection = connect_database(db_path)

    try:
        cursor = connection.execute(
            """
            INSERT INTO datasets (source_file, record_count)
            VALUES (?, ?)
            """,
            (str(source_file), len(records))
        )

        dataset_id = cursor.lastrowid

        connection.executemany(
            """
            INSERT INTO records (
                dataset_id,
                row_number,
                data_json
            )
            VALUES (?, ?, ?)
            """,
            [
                (dataset_id, index, json.dumps(record))
                for index, record in enumerate(records, start=1)
            ]
        )

        connection.commit()
        return dataset_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_dataset_records(db_path, dataset_id):
    connection = connect_database(db_path)

    try:
        rows = connection.execute(
            """
            SELECT data_json
            FROM records
            WHERE dataset_id = ?
            ORDER BY row_number
            """,
            (dataset_id,)
        ).fetchall()

        return [json.loads(row[0]) for row in rows]

    finally:
        connection.close()


def list_datasets(db_path):
    connection = connect_database(db_path)

    try:
        rows = connection.execute(
            """
            SELECT id, source_file, imported_at, record_count
            FROM datasets
            ORDER BY id DESC
            """
        ).fetchall()

        return [
            {
                "id": row[0],
                "source_file": row[1],
                "imported_at": row[2],
                "record_count": row[3]
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_dataset(db_path, dataset_id):
    connection = connect_database(db_path)

    try:
        row = connection.execute(
            """
            SELECT id, source_file, imported_at, record_count
            FROM datasets
            WHERE id = ?
            """,
            (dataset_id,)
        ).fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "source_file": row[1],
            "imported_at": row[2],
            "record_count": row[3]
        }

    finally:
        connection.close()


def delete_dataset(db_path, dataset_id):
    connection = connect_database(db_path)

    try:
        cursor = connection.execute(
            """
            DELETE FROM datasets
            WHERE id = ?
            """,
            (dataset_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()