from functions import connect_with_role, use_context
from functions import ACCOUNT
from functions import WH_NAME, DW_NAME, RAW_SCHEMA
from functions import ROLE_TRANSFORMER, USER_DEV, PASSWORD_DEV


def create_table(cur):
    cur.execute("CREATE FILE FORMAT IF NOT EXISTS parquet_format TYPE = 'PARQUET'")
    
    cur.execute("SELECT column_name, type FROM TABLE(INFER_SCHEMA(LOCATION=>'@~/',FILE_FORMAT=>'parquet_format'))")
    schema = cur.fetchall()
    columns = [f"{col_name} {col_type}" for col_name, col_type in schema]
    
    create_sql = f"CREATE TABLE IF NOT EXISTS yellow_taxi_trips_raw ({', '.join(columns)})"
    cur.execute(create_sql)
    cur.execute("ALTER TABLE yellow_taxi_trips_raw ADD COLUMN IF NOT EXISTS filename VARCHAR(255)")
    print("✓ Table créée dynamiquement")

def copy_file_to_table_and_count(cur, filename):
    print(f"🚀 Chargement de {filename}...")

    cur.execute("SELECT COUNT(*) FROM yellow_taxi_trips_raw")
    before = cur.fetchone()[0]

    cur.execute(f"""
        COPY INTO yellow_taxi_trips_raw 
        FROM '@~/{filename}'
        FILE_FORMAT=(FORMAT_NAME='parquet_format')
        MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE
    """)

    cur.execute("SELECT COUNT(*) FROM yellow_taxi_trips_raw")
    after = cur.fetchone()[0]

    rows_loaded = after - before
    return rows_loaded

def update_metadata(cur, filename, rows_loaded):  
    cur.execute("""
        UPDATE file_loading_metadata 
        SET rows_loaded = %s, load_status = 'SUCCESS' 
        WHERE file_name = %s
    """, (rows_loaded, filename))
    print(f"✅ {filename} chargé ({rows_loaded} lignes)")

def cleanup_stage_file(cur, filename):
    cur.execute(f"REMOVE @~/{filename}")
    print(f"✅ {filename} supprimé du stage")

def handle_loading_error(cur, filename, error):
    print(f"❌ Erreur de chargement {filename}: {error}")
    cur.execute("UPDATE file_loading_metadata SET load_status='FAILED_LOAD' WHERE file_name=%s", (filename,))

def main():
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)
    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        create_table(cur)
        
        cur.execute("SELECT file_name FROM file_loading_metadata WHERE load_status='STAGED'")
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