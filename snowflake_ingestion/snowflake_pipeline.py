import os
import requests
import shutil
from lxml import html
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

WH_NAME = os.getenv('WH_NAME')
DW_NAME = os.getenv('DW_NAME')
RAW_SCHEMA_NAME = os.getenv('RAW_SCHEMA_NAME')



def setup_data_warehouse():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        autocommit=True,
        connection_timeout=30,
        network_timeout=60
    )
    with conn.cursor() as cur:
        cur.execute(f"CREATE WAREHOUSE IF NOT EXISTS {WH_NAME} WITH WAREHOUSE_SIZE = 'X-SMALL' AUTO_SUSPEND = 1 AUTO_RESUME = TRUE")
        cur.execute(f"USE WAREHOUSE {WH_NAME}")
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DW_NAME}")
        cur.execute(f"USE DATABASE {DW_NAME}")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA_NAME}")
        cur.execute("CREATE SCHEMA IF NOT EXISTS STAGING")
        cur.execute("CREATE SCHEMA IF NOT EXISTS FINAL")
        cur.execute(f"USE SCHEMA {RAW_SCHEMA_NAME}")
        cur.execute("CREATE OR REPLACE FILE FORMAT parquet_format TYPE = 'PARQUET'")
        print("✓ Architecture DW créée")
    return conn



def get_parquet_links():
    url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2025') or contains(@href, '2024'))]"
    filtered_links = tree.xpath(xpath_query)
    return [link.get('href') for link in filtered_links if link.get('href') and link.get('href').endswith('.parquet')]



def create_table(cur):
    cur.execute("""
        SELECT column_name, type
        FROM TABLE(INFER_SCHEMA(
            LOCATION=>'@~/',
            FILE_FORMAT=>'parquet_format'
        ))
    """)

    schema = cur.fetchall()
    columns = []

    for col_name, col_type in schema:
        columns.append(f"{col_name} {col_type}")

    create_sql = f"CREATE TABLE IF NOT EXISTS yellow_taxi_trips_raw ({', '.join(columns)})"
    cur.execute(create_sql)
    # Ajouter la colonne filename
    cur.execute("ALTER TABLE yellow_taxi_trips_raw ADD COLUMN IF NOT EXISTS filename VARCHAR(255)")
    print("✓ Table créée dynamiquement")



def create_meta_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS file_loading_metadata (
            file_url VARCHAR(500),
            file_name VARCHAR(255),
            year NUMBER,
            month NUMBER,
            rows_loaded NUMBER,
            load_status VARCHAR(50),
            load_timestamp TIMESTAMP_TZ DEFAULT CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())
        )
    """)



def download_and_upload_file(cur, file_url, filename, temp_dir="temp_files"):
    """Télécharge et upload un fichier vers Snowflake"""
    tmp_path = f"{temp_dir}/{filename}"
    
    print(f"📥 Téléchargement de {filename}...")
    response = requests.get(file_url)
    response.raise_for_status()

    with open(tmp_path, 'wb') as f:
        f.write(response.content)
    
    print(f"📤 Upload vers Snowflake...")
    put_command = f"PUT 'file://{os.path.abspath(tmp_path)}' @~ AUTO_COMPRESS=FALSE"
    cur.execute(put_command)
    
    return tmp_path



def load_into_table(cur, filename):
    """Charge les données dans la table et retourne le nombre de lignes"""
    print(f"🚀 Chargement dans la table...")
    copy_command = f"""
    COPY INTO yellow_taxi_trips_raw 
    FROM '@~/{filename}'
    FILE_FORMAT = (FORMAT_NAME = 'parquet_format')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
    """
    cur.execute(copy_command)

    cur.execute("UPDATE yellow_taxi_trips_raw SET filename = %s WHERE filename IS NULL", (filename,))
    cur.execute("SELECT COUNT(*) FROM yellow_taxi_trips_raw WHERE filename = %s", (filename,))
    return cur.fetchone()[0]



def insert_metadata(cur, file_url, filename, rows_loaded, status):
    """Insère les métadonnées de chargement"""
    parts = filename.replace('yellow_tripdata_', '').replace('.parquet', '').split('-')
    year = int(parts[0]) if len(parts) > 0 else None
    month = int(parts[1]) if len(parts) > 1 else None
    
    cur.execute("""
        INSERT INTO file_loading_metadata 
        (file_url, file_name, year, month, rows_loaded, load_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (file_url, filename, year, month, rows_loaded, status))



def use_context(cur):
    cur.execute(f"USE WAREHOUSE {WH_NAME}")
    cur.execute(f"USE DATABASE {DW_NAME}")
    cur.execute(f"USE SCHEMA {RAW_SCHEMA_NAME}")



def upload_and_load_parquet(conn, file_urls):
    os.makedirs("temp_files", exist_ok=True)
    
    try:
        with conn.cursor() as cur:
            use_context(cur)
            create_meta_table(cur)
            
            for file_url in file_urls:
                try:
                    filename = file_url.split('/')[-1]
                    # Vérifier si déjà chargé
                    cur.execute("SELECT file_name FROM file_loading_metadata WHERE file_name = %s AND load_status = 'SUCCESS'", (filename,))
                    if cur.fetchone():
                        print(f"⏭️  {filename} déjà chargé - skip")
                        continue
                    tmp_path = download_and_upload_file(cur, file_url,filename)
                    create_table(cur)
                    rows_loaded = load_into_table(cur, filename)
                    insert_metadata(cur, file_url, filename, rows_loaded, 'SUCCESS')
                    print(f"✅ {rows_loaded} lignes chargées")
                    
                except Exception as e:
                    insert_metadata(cur, file_url, filename, 0, 'FAILED')
                    print(f"❌ Erreur avec {filename}: {e}")
                    
                finally:
                    # Nettoyage (suppression dans dossier et stage)
                    if 'tmp_path' in locals() and os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                    cur.execute(f"REMOVE @~/{filename}")
    
    finally:
        # Nettoyage final du dossier
        if os.path.exists("temp_files"):
            shutil.rmtree("temp_files")
            print("📁 Dossier temp_files supprimé")



def verify_data_loaded(conn):
    with conn.cursor() as cur:
        use_context(cur)
        cur.execute("SELECT COUNT(*) FROM yellow_taxi_trips_raw")
        total_rows = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM file_loading_metadata WHERE load_status = 'SUCCESS'")
        success_files = cur.fetchone()[0]
        
        print(f"\n📊 DONNEES DANS RAW: {total_rows:,} lignes - {success_files} fichiers")
        
        if total_rows > 0:
            cur.execute("SELECT * FROM yellow_taxi_trips_raw LIMIT 2")
            sample = cur.fetchall()
            print("Aperçu des données (2 premières lignes):")
            for row in sample:
                print(f"  {row}")



def main():
    conn = None
    try:
        conn = setup_data_warehouse()
        file_urls = get_parquet_links()
        print(f"📁 {len(file_urls)} fichiers Parquet trouvés pour 2024-2025")
        if not file_urls:
            print("Aucun fichier scrappé")
            return
            
        upload_and_load_parquet(conn, file_urls)
        # verify_data_loaded(conn)
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
    finally:
        if conn:
            conn.close()
            print("🔌 Connexion Snowflake fermée")



if __name__ == "__main__":
    main()