CREATE TABLE IF NOT EXISTS { METADATA_TABLE } (
    file_url VARCHAR(500),
    file_name VARCHAR(250),
    year NUMBER,
    month NUMBER,
    rows_loaded NUMBER,
    load_status VARCHAR(10),
    load_timestamp TIMESTAMP_TZ DEFAULT CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())
)