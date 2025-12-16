from typing import List, Tuple
from snowflake.connector.cursor import SnowflakeCursor
import snowflake_ingestion.functions as functions

functions.config_logger()
logger = functions.logging.getLogger(__name__)

SQL_DIR = functions.SQL_BASE_DIR / "loading"

def create_table(cur: SnowflakeCursor) -> List[Tuple[str, str]]:
    """Create or verify the RAW table dynamically based on staged file schema.
    Executes SQL to detect the file schema in the Snowflake stage,
    creates the RAW table if it does not exist, and adds the filename
    column if needed.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.

    Returns:
        list: The table schema detected from staged files
    """
    logger.info(f"📋 Vérification/Création dynamique de la table {functions.RAW_TABLE}")
    functions.run_sql_file(cur, SQL_DIR / "detect_file_schema_stage.sql")
    schema = cur.fetchall()
    seen = set()
    table_schema: List[Tuple[str, str]] = []
    for col_name, col_type in schema:
        if col_name.lower() not in seen:
            seen.add(col_name.lower())
            table_schema.append((col_name, col_type))
    if len(table_schema) == 0:
        logger.warning("⚠️  Aucune donnée dans le STAGE")
        return table_schema
    functions.run_sql_file(cur, SQL_DIR / "create_sequence.sql")

    columns = [f"TRIP_ID NUMBER"] + [f"{col_name} {col_type}" for col_name, col_type in table_schema]
    if len(columns) != 0:
        create_sql = f"CREATE TABLE IF NOT EXISTS {functions.RAW_TABLE} ({', '.join(columns)})"
        cur.execute(create_sql)
        functions.run_sql_file(cur, SQL_DIR / "add_filename_to_raw_table.sql")
        logger.info(f"✅ Table {functions.RAW_TABLE} prête")
    else:
        logger.warning(f"⚠️  Aucune donnée dans le STAGE")
    return table_schema

def copy_file_to_table_and_count(cur: SnowflakeCursor, filename: str, table_schema: List[Tuple[str, str]]) -> int:
    """Load a Parquet file from stage into the RAW table and count inserted rows.
    Uses COPY INTO with transformation to generate TRIP_ID using sequence and 
    maps Parquet columns using positional references.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
        filename (str): Name of the staged file to load.
        table_schema (list): Pre-detected schema from create_table function.

    Returns:
        int: Number of rows inserted into the RAW table.
    """
    logger.info(f"🚀 Chargement de {filename} dans {functions.RAW_TABLE}...")
    column_names = [col[0].replace("airport_fee", "Airport_fee") for col in table_schema]
    select_columns = [f"$1:{col_name}" for col_name in column_names]
    copy_sql = f"""
        COPY INTO {functions.RAW_TABLE} (TRIP_ID, {', '.join(column_names)}, FILENAME)
        FROM (
            SELECT 
                {functions.ID_SEQUENCE}.NEXTVAL,
                {', '.join(select_columns)},
                '{filename}'
            FROM '@~/{filename}'
        )
        FILE_FORMAT=(FORMAT_NAME='{functions.DW_NAME}.{functions.RAW_SCHEMA}.{functions.PARQUET_FORMAT}')
        FORCE = TRUE
    """
    cur.execute(copy_sql)
    result = cur.fetchone()
    if result and len(result) > 3:
        rows_loaded = result[3]
    else:
        rows_loaded = 0
    s = "s" if rows_loaded >= 2 else ""
    logger.info(f"✅ {filename} chargé ({rows_loaded} ligne{s})")
    return rows_loaded

def update_metadata(cur: SnowflakeCursor, filename: str, rows_loaded: int) -> None:
    """Update the metadata table after successful file loading.
    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
        filename (str): Name of the loaded file.
        rows_loaded (int): Number of rows successfully inserted.
    """
    cur.execute(
        f"""
        UPDATE {functions.METADATA_TABLE} 
        SET rows_loaded = %s, load_status = 'SUCCESS' 
        WHERE file_name = %s
        """,
        (rows_loaded, filename),
    )
    logger.debug(f"🚀 Chargement de {functions.METADATA_TABLE}")

def cleanup_stage_file(cur: SnowflakeCursor, filename: str) -> None:
    """Remove the processed file from the Snowflake stage.
    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
        filename (str): Name of the file to delete from the stage.
    """
    cur.execute(f"REMOVE @~/{filename}")
    logger.info(f"✅ {filename} supprimé du stage")

def handle_loading_error(cur: SnowflakeCursor, filename: str, error: Exception) -> None:
    """Handle errors occurring during file loading into the RAW table.
    Logs the error and updates the metadata table to mark the file
    as failed during the load step.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
        filename (str): Name of the file that failed to load.
        error (Exception): Exception raised during the loading process.
    """
    logger.error(f"❌ Erreur de chargement {filename}: {error}")
    logger.debug(f"🚀 Chargement de {functions.METADATA_TABLE}")
    cur.execute(
        f"UPDATE {functions.METADATA_TABLE} SET load_status='FAILED_LOAD' WHERE file_name=%s",
        (filename,),
    )

def main() -> None:
    """Main process for loading staged Parquet files into the RAW table.
    Connects to Snowflake, ensures the RAW table exists, retrieves staged files,
    loads each into the RAW table, updates metadata, and cleans up stage files.
    """
    conn = functions.connect_with_role(functions.USER_DEV, functions.PASSWORD_DEV, functions.ACCOUNT, functions.ROLE_TRANSFORMER)
    with conn.cursor() as cur:
        functions.use_context(cur, functions.WH_NAME, functions.DW_NAME, functions.RAW_SCHEMA)
        table_schema = create_table(cur)
        
        logger.info("🔍 Analyse des fichiers dans le STAGE")
        functions.run_sql_file(cur, SQL_DIR / "select_filename_from_meta_staged.sql")
        staged_files = cur.fetchall()

        for (filename,) in staged_files:
            try:
                rows_loaded = copy_file_to_table_and_count(cur, filename, table_schema)
                update_metadata(cur, filename, rows_loaded)
                cleanup_stage_file(cur, filename)
            except Exception as e:
                handle_loading_error(cur, filename, e)
                
    conn.close()

if __name__ == "__main__":
    main()