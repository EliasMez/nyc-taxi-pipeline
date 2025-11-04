import requests
from lxml import html
from functions import *

config_logger()
logger = logging.getLogger(__name__)

SQL_DIR = SQL_BASE_DIR / "02_scraping"


def get_parquet_links():
    logger.info("🌐 Début du scraping des données NYC Taxi")
    url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2025') or contains(@href, '2024'))]"
    filtered_links = tree.xpath(xpath_query)
    return [link.get('href') for link in filtered_links if link.get('href') and link.get('href').endswith('.parquet')]


def setup_meta_table(cur):
    logger.info("📋 Vérification/Création de la table de metadata")
    sql_file = SQL_DIR / "setup_meta_table.sql"
    run_sql_file(cur, sql_file)
    logger.info("✅ Table de metadata prête")

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
                
                logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
                cur.execute(f"""
                    INSERT INTO {METADATA_TABLE} (file_url, file_name, year, month, rows_loaded, load_status)
                    VALUES (%s, %s, %s, %s, 0, 'SCRAPED')
                """, (url, filename, year, month))
            else:
                logger.info(f"⏭️  {filename} déjà référencé")
            
            if not new_file_detected:
                logger.debug("🔍 Analyse des fichiers SCRAPED")
                run_sql_file(cur, SQL_DIR / "count_new_files.sql")
                if cur.fetchone()[0] > 0:
                    new_file_detected = True

    conn.close()

    if not new_file_detected:
        logger.warning("⚠️  Aucun nouveau fichier à charger.")
    
    logger.info("✅ Scraping terminé")

if __name__ == "__main__":
    main()