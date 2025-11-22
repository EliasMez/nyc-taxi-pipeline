import requests
import tempfile
from snowflake_ingestion.functions import *

config_logger()
logger = logging.getLogger(__name__)

SQL_DIR = SQL_BASE_DIR / "staging"


def download_and_upload_file(cur, file_url, filename) -> None:
    """Download a Parquet file from URL and upload it directly to Snowflake stage.
    
    This function streams the file content directly to Snowflake without persisting
    it permanently on disk. It uses a temporary file that is automatically deleted
    after the upload completes, ensuring no residual files are left behind.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor 
            used to execute the PUT command.
        file_url (str): HTTPS URL of the Parquet file to download.
        filename (str): Destination filename in the Snowflake stage.

    Raises:
        requests.HTTPError: If the HTTP request fails (non-200 status code).
        snowflake.connector.errors.Error: If the Snowflake PUT command fails.
    """
    logger.info(f"📥 Téléchargement de {filename}...")
    response = requests.get(file_url)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix='.parquet', delete=True) as tmp_file:
        tmp_file.write(response.content)
        tmp_file.flush()   
        logger.info(f"📤 Upload vers Snowflake...")
        cur.execute(f"PUT 'file://{tmp_file.name}' @~/{filename} AUTO_COMPRESS=FALSE")
    logger.info(f"✅ {filename} uploadé et fichier temporaire nettoyé")


def main():
    """Main staging process for Parquet files.

    Connects to Snowflake, retrieves metadata for scraped files, downloads
    each file, uploads it to the stage, and updates the metadata table
    with the appropriate load status.
    """
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)

    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        logger.debug("📥 Récupération des URLs et noms des fichiers scrappés")
        run_sql_file(cur, SQL_DIR / "select_file_url_name_from_meta_scraped.sql")
        scraped_files = cur.fetchall()
        scraped_files_count = len(scraped_files)
        if scraped_files_count == 0:
            logger.warning(f"⚠️  Aucun fichier à uploader")
        else :
            logger.info(f"📦 {scraped_files_count} fichiers à uploader")

        for file_url, filename in scraped_files:
            try:
                download_and_upload_file(cur, file_url, filename)
                logger.info(f"✅ {filename} uploadé")
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='STAGED' WHERE file_name=%s", (filename,))
                logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
            except Exception as e:
                logger.error(f"❌ Erreur upload {filename}: {e}")
                logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='FAILED_STAGE' WHERE file_name=%s", (filename,))
    conn.close()

if __name__ == "__main__":
    main()
