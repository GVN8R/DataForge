DEFAULT_RULES = {
    "required_columns": [],
    "numeric_columns": [],
    "unique_columns": []
}

WEATHER_RULES = {
    "required_columns": ["date", "temperature"],
    "numeric_columns": ["temperature", "precipitation"],
    "unique_columns": ["date"]
}

DEFAULT_TRANSFORMATION_RULES = {
    "missing_markers": {"", "n/a", "na", "unknown", "null"},
    "numeric_columns": [],
    "date_columns": [],
    "date_format": None
}

WEATHER_TRANSFORMATION_RULES = {
    "missing_markers": {"", "n/a", "na", "unknown", "null"},
    "numeric_columns": ["temperature", "precipitation"],
    "date_columns": ["date"],
    "date_format": "%Y-%m-%d"
}