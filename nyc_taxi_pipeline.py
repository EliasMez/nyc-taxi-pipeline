import os
import requests
import shutil
from lxml import html
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def setup_data_warehouse():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        autocommit=True
    )
    
    with conn.cursor() as cur:
        cur.execute("CREATE WAREHOUSE IF NOT EXISTS NYC_WH WITH WAREHOUSE_SIZE = 'X-SMALL' AUTO_SUSPEND = 1 AUTO_RESUME = TRUE")
        cur.execute("USE WAREHOUSE NYC_WH")
        cur.execute("CREATE DATABASE IF NOT EXISTS NYC_TAXI_DW")
        cur.execute("USE DATABASE NYC_TAXI_DW")
        cur.execute("CREATE SCHEMA IF NOT EXISTS RAW")
        cur.execute("CREATE SCHEMA IF NOT EXISTS STAGING")
        cur.execute("CREATE SCHEMA IF NOT EXISTS FINAL")
        
        cur.execute("CREATE OR REPLACE STAGE raw_parquet_stage")
        cur.execute("CREATE OR REPLACE FILE FORMAT parquet_format TYPE = 'PARQUET'")
        
        print("✓ Architecture DW créée")
    
    return conn

def create_table_dynamically(conn):
    with conn.cursor() as cur:
        cur.execute("USE DATABASE NYC_TAXI_DW")
        cur.execute("USE SCHEMA RAW")
        
        cur.execute("""
            SELECT column_name, type
            FROM TABLE(INFER_SCHEMA(
                LOCATION=>'@raw_parquet_stage/',
                FILE_FORMAT=>'parquet_format'
            ))
        """)
        schema = cur.fetchall()
        
        columns = []
        for col_name, col_type in schema:
            columns.append(f"{col_name} {col_type}")
        columns.append("filename VARCHAR(255)")
        columns.append("load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()")
        
        create_sql = f"CREATE OR REPLACE TABLE yellow_taxi_trips_raw ({', '.join(columns)})"
        cur.execute(create_sql)
        print("✓ Table créée dynamiquement")

def get_parquet_links():
    url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2025') or contains(@href, '2024'))]"
    filtered_links = tree.xpath(xpath_query)
    
    return [link.get('href') for link in filtered_links if link.get('href') and link.get('href').endswith('.parquet')]

def upload_and_load_parquet(conn, file_urls):
    os.makedirs("temp_files", exist_ok=True)
    
    with conn.cursor() as cur:
        cur.execute("USE DATABASE NYC_TAXI_DW")
        cur.execute("USE SCHEMA RAW")
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS file_loading_metadata (
                file_url VARCHAR(500),
                file_name VARCHAR(255),
                year NUMBER,
                month NUMBER,
                rows_loaded NUMBER,
                load_status VARCHAR(50),
                load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        
        for file_url in file_urls:
            try:
                filename = file_url.split('/')[-1]
                
                # Vérifier si déjà chargé
                cur.execute("SELECT file_name FROM file_loading_metadata WHERE file_name = %s AND load_status = 'SUCCESS'", (filename,))
                if cur.fetchone():
                    print(f"⏭️  {filename} déjà chargé - skip")
                    continue
                
                print(f"📥 Téléchargement de {filename}...")
                
                response = requests.get(file_url)
                response.raise_for_status()

                tmp_path = f"temp_files/{filename}"
                with open(tmp_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"📤 Upload vers Snowflake...")
                put_command = f"PUT 'file://{os.path.abspath(tmp_path)}' @raw_parquet_stage AUTO_COMPRESS=FALSE"
                cur.execute(put_command)
                
                create_table_dynamically(conn)
                
                print(f"🚀 Chargement dans la table...")
                copy_command = f"""
                COPY INTO yellow_taxi_trips_raw 
                FROM '@raw_parquet_stage/{filename}'
                FILE_FORMAT = (FORMAT_NAME = 'parquet_format')
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
                """
                cur.execute(copy_command)
                rows_loaded = cur.rowcount
                
                os.unlink(tmp_path)
                cur.execute(f"REMOVE @raw_parquet_stage/{filename}")
                
                parts = filename.replace('yellow_tripdata_', '').replace('.parquet', '').split('-')
                year = int(parts[0]) if len(parts) > 0 else None
                month = int(parts[1]) if len(parts) > 1 else None
                
                cur.execute("""
                    INSERT INTO file_loading_metadata 
                    (file_url, file_name, year, month, rows_loaded, load_status)
                    VALUES (%s, %s, %s, %s, %s, 'SUCCESS')
                """, (file_url, filename, year, month, rows_loaded))
                
                print(f"✅ {rows_loaded} lignes chargées")

                # supression table temporaire
                if os.path.exists("temp_files"):
                    shutil.rmtree("temp_files")
                    print("📁 Dossier temp_files supprimé")
                
            except Exception as e:
                print(f"❌ Erreur: {e}")
                try:
                    cur.execute("""
                        INSERT INTO file_loading_metadata 
                        (file_url, file_name, year, month, rows_loaded, load_status)
                        VALUES (%s, %s, %s, %s, %s, 'FAILED')
                    """, (file_url, filename, year, month, 0))
                except:
                    pass

def verify_data_loaded(conn):
    with conn.cursor() as cur:
        cur.execute("USE DATABASE NYC_TAXI_DW")
        cur.execute("USE SCHEMA RAW")
        
        cur.execute("SELECT COUNT(*) FROM yellow_taxi_trips_raw")
        total_rows = cur.fetchone()[0]
        if total_rows > 0:
            cur.execute("SELECT * FROM yellow_taxi_trips_raw LIMIT 2")
            sample = cur.fetchall()
            print("Aperçu des données:")
            for row in sample:
                print(f"  {row}")
        
        cur.execute("SELECT COUNT(*) FROM file_loading_metadata WHERE load_status = 'SUCCESS'")
        success_files = cur.fetchone()[0]
        
        print(f"\n📊 DONNEES DANS RAW: {total_rows:,} lignes - {success_files} fichiers")

def main():
    conn = None
    try:
        conn = setup_data_warehouse()
        file_urls = get_parquet_links()
        print(f"📁 {len(file_urls)} fichiers trouvés")
        upload_and_load_parquet(conn, file_urls)
        verify_data_loaded(conn)
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()