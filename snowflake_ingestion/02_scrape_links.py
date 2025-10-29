import requests
from lxml import html
from functions import connect_with_role, use_context
from functions import ACCOUNT
from functions import WH_NAME, DW_NAME, RAW_SCHEMA, METADATA_TABLE
from functions import ROLE_TRANSFORMER, USER_DEV, PASSWORD_DEV
from functions import config_logger
import logging

config_logger()
logger = logging.getLogger(__name__)

def get_parquet_links():
    url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2025') or contains(@href, '2024'))]"
    filtered_links = tree.xpath(xpath_query)
    return [link.get('href') for link in filtered_links if link.get('href') and link.get('href').endswith('.parquet')]


def setup_meta_table(cur):
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {METADATA_TABLE} (
            file_url VARCHAR(500),
            file_name VARCHAR(255),
            year NUMBER,
            month NUMBER,
            rows_loaded NUMBER,
            load_status VARCHAR(50),
            load_timestamp TIMESTAMP_TZ DEFAULT CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())
        )
    """)

def main():
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)
    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        setup_meta_table(cur)

        links = get_parquet_links()
        logger.info(f"📎 {len(links)} liens trouvés")
        new_file_detected = False

        for url in links:
            filename = url.split('/')[-1]
            cur.execute(f"SELECT 1 FROM {METADATA_TABLE} WHERE file_name = %s", (filename,))
            if not cur.fetchone():
                logger.info(f"➕ Nouveau fichier détecté : {filename}")
                new_file_detected = True
                
                # Extraire année et mois depuis le filename
                parts = filename.replace('yellow_tripdata_', '').replace('.parquet', '').split('-')
                year = int(parts[0]) if len(parts) > 0 else None
                month = int(parts[1]) if len(parts) > 1 else None
                
                cur.execute(f"""
                    INSERT INTO {METADATA_TABLE} (file_url, file_name, year, month, rows_loaded, load_status)
                    VALUES (%s, %s, %s, %s, 0, 'SCRAPED')
                """, (url, filename, year, month))
            else:
                logger.info(f"⏭️ {filename} déjà référencé")
            
            # Vérifie s'il reste des fichiers en statut SCRAPED ou STAGED à traiter
            if not new_file_detected:
                cur.execute(f"SELECT COUNT(*) FROM {METADATA_TABLE} WHERE load_status IN ('SCRAPED', 'STAGED')")
                if cur.fetchone()[0] > 0:
                    new_file_detected = True

    conn.close()

    print(f"new_file_detected={new_file_detected}")
    if not new_file_detected:
        logger.error("❌ Aucun nouveau fichier à charger, arrêt du workflow.")
    
    logger.info("✅ Scraping terminé")

if __name__ == "__main__":
    main()