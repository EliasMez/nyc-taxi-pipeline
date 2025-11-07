import requests
from lxml import html
from functions import *
from datetime import datetime

config_logger()
logger = logging.getLogger(__name__)

SQL_DIR = SQL_BASE_DIR / "02_scraping"

current_year = datetime.now().year
current_month = datetime.now().month

def get_scraping_year():
    default_year = current_year - 1 if current_month <= 3 else current_year
    if SCRAPING_YEAR == "":
        return default_year
    else:
        try:
            int_year = int(SCRAPING_YEAR)
        except:
            logger.error(f"\"SCRAPING_YEAR = {SCRAPING_YEAR}\" n'est pas une année valide !")
            logger.warning(f"L'année du scraping a été réinitialisée à {default_year}")
            return default_year
        
        if int_year < 2009 or int_year > current_year:
            logger.error(f"\"SCRAPING_YEAR = {SCRAPING_YEAR}\" l'année du scraping doit être compris entre 2009 et {current_year} inclus!")
            logger.warning(f"L'année du scraping a été réinitialisée à {default_year}")
            return default_year
        logger.info(f"Les fichiers seront scrapés à partir de l'année {default_year}")
        return int_year
     

def get_xpath():
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and ("
    get_contains = lambda year: f"contains(@href, '{year}')"
    contains_list = [get_contains(year) for year in range(get_scraping_year(),current_year+1)]
    xpath_query+= " or ".join(contains_list) + ")]"
    return xpath_query


def get_parquet_links():
    logger.info("🌐 Début du scraping des données NYC Taxi")
    url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath_query = get_xpath()
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