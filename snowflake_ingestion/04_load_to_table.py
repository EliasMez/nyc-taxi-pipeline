from functions import connect_with_role, use_context
from functions import ACCOUNT
from functions import WH_NAME, DW_NAME, RAW_SCHEMA, RAW_TABLE, METADATA_TABLE, PARQUET_FORMAT
from functions import ROLE_TRANSFORMER, USER_DEV, PASSWORD_DEV


def create_table(cur):    
    cur.execute(f"SELECT column_name, type FROM TABLE(INFER_SCHEMA(LOCATION=>'@~/',FILE_FORMAT=>'{DW_NAME}.{RAW_SCHEMA}.{PARQUET_FORMAT}'))")
    schema = cur.fetchall()
    columns = [f"{col_name} {col_type}" for col_name, col_type in schema]
    if len(columns)!=0 :
        create_sql = f"CREATE TABLE IF NOT EXISTS {RAW_TABLE} ({', '.join(columns)})"
        cur.execute(create_sql)
        cur.execute(f"ALTER TABLE {RAW_TABLE} ADD COLUMN IF NOT EXISTS filename VARCHAR(255)")
        print("✓ Table créée dynamiquement")

def copy_file_to_table_and_count(cur, filename):
    print(f"🚀 Chargement de {filename}...")

    cur.execute(f"SELECT COUNT(*) FROM {RAW_TABLE}")
    before = cur.fetchone()[0]

    cur.execute(f"""
        COPY INTO {RAW_TABLE} 
        FROM '@~/{filename}'
        FILE_FORMAT=(FORMAT_NAME='{DW_NAME}.{RAW_SCHEMA}.{PARQUET_FORMAT}')
        MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
    """)

    cur.execute(f"SELECT COUNT(*) FROM {RAW_TABLE}")
    after = cur.fetchone()[0]

    rows_loaded = after - before
    return rows_loaded

def update_metadata(cur, filename, rows_loaded):  
    cur.execute(f"""
        UPDATE {METADATA_TABLE} 
        SET rows_loaded = %s, load_status = 'SUCCESS' 
        WHERE file_name = %s
    """, (rows_loaded, filename))
    print(f"✅ {filename} chargé ({rows_loaded} lignes)")

def cleanup_stage_file(cur, filename):
    cur.execute(f"REMOVE @~/{filename}")
    print(f"✅ {filename} supprimé du stage")

def handle_loading_error(cur, filename, error):
    print(f"❌ Erreur de chargement {filename}: {error}")
    cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='FAILED_LOAD' WHERE file_name=%s", (filename,))

def main():
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)
    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        create_table(cur)
        
        cur.execute(f"SELECT file_name FROM {METADATA_TABLE} WHERE load_status='STAGED'")
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