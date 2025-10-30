from functions import *

config_logger()
logger = logging.getLogger(__name__)

SQL_DIR = SQL_BASE_DIR / "04_load"


def create_table(cur):
    logger.info(f"📋 Vérification/Création dynamique de la table {RAW_TABLE}")
    run_sql_file(cur, SQL_DIR / "detect_file_schema_stage.sql")
    schema = cur.fetchall()
    columns = [f"{col_name} {col_type}" for col_name, col_type in schema]
    if len(columns)!=0 :
        create_sql = f"CREATE TABLE IF NOT EXISTS {RAW_TABLE} ({', '.join(columns)})"
        cur.execute(create_sql)
        run_sql_file(cur, SQL_DIR / "add_filename_to_raw_table.sql")
        logger.info(f"✅ Table {RAW_TABLE} prête")
    else :
        logger.warning(f"⚠️ Aucune donnée dans le STAGE")



def copy_file_to_table_and_count(cur, filename):
    logger.info(f"🚀 Chargement de {filename} dans {RAW_TABLE}...")

    run_sql_file(cur, SQL_DIR / "count_rows_from_raw_table.sql")
    before = cur.fetchone()[0]

    cur.execute(f"""
        COPY INTO {RAW_TABLE} 
        FROM '@~/{filename}'
        FILE_FORMAT=(FORMAT_NAME='{DW_NAME}.{RAW_SCHEMA}.{PARQUET_FORMAT}')
        MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
    """)

    run_sql_file(cur, SQL_DIR / "count_rows_from_raw_table.sql")
    after = cur.fetchone()[0]

    rows_loaded = after - before
    logger.info(f"✅ {filename} chargé ({rows_loaded} lignes)")
    return rows_loaded



def update_metadata(cur, filename, rows_loaded):  
    cur.execute(f"""
        UPDATE {METADATA_TABLE} 
        SET rows_loaded = %s, load_status = 'SUCCESS' 
        WHERE file_name = %s
    """, (rows_loaded, filename))
    logger.debug(f"🚀 Chargement de {METADATA_TABLE}")



def cleanup_stage_file(cur, filename):
    cur.execute(f"REMOVE @~/{filename}")
    logger.info(f"✅ {filename} supprimé du stage")



def handle_loading_error(cur, filename, error):
    logger.error(f"❌ Erreur de chargement {filename}: {error}")
    logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
    cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='FAILED_LOAD' WHERE file_name=%s", (filename,))



def main():
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)
    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        create_table(cur)
        
        logger.info("🔍 Analyse des fichiers dans le STAGE")
        run_sql_file(cur, SQL_DIR / "select_filename_from_meta_staged.sql")
        staged_files = cur.fetchall()

        for (filename,) in staged_files:
            try:
                rows_loaded = copy_file_to_table_and_count(cur, filename)
                update_metadata(cur, filename, rows_loaded)
                cleanup_stage_file(cur, filename)
            except Exception as e:
                handle_loading_error(cur, filename, e)
                
    conn.close()

if __name__ == "__main__":
    main()