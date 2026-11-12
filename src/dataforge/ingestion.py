import csv
from pathlib import Path


def read_csv(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or missing headers.")
        
        headers = [header.strip() for header in reader.fieldnames]

        if any(not header for header in headers):
            raise ValueError("CSV contains an empty column name.")
        
        if len(headers) != len(set(headers)):
            raise ValueError("CSV contains duplicate column names.")
        
        records = []

        for row in reader:
            if None in row:
                raise ValueError("CSV row contains more values than headers.")
            
            records.append(row)

        return records