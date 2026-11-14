from pathlib import Path
import sqlite3


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