import os
import requests
import shutil
from functions import *

config_logger()
logger = logging.getLogger(__name__)

SQL_DIR = SQL_BASE_DIR / "03_stage"


def download_and_upload_file(cur, file_url, filename, temp_dir="temp_files"):
    os.makedirs(temp_dir, exist_ok=True)
    tmp_path = f"{temp_dir}/{filename}"
    logger.info(f"📥 Téléchargement de {filename}...")
    response = requests.get(file_url)
    response.raise_for_status()
    with open(tmp_path, 'wb') as f:
        f.write(response.content)

    logger.info(f"📤 Upload vers Snowflake...")
    cur.execute(f"PUT 'file://{os.path.abspath(tmp_path)}' @~ AUTO_COMPRESS=FALSE")
    return tmp_path

def main():
    conn = connect_with_role(USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER)

    with conn.cursor() as cur:
        use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA)
        logger.debug("📥 Récupération des URLs et noms des fichiers scrappés")
        run_sql_file(cur, SQL_DIR / "select_file_url_name_from_meta_scraped.sql")
        scraped_files = cur.fetchall()
        logger.info(f"📦 {len(scraped_files)} fichiers à uploader")

        for file_url, filename in scraped_files:
            try:
                tmp_path = download_and_upload_file(cur, file_url, filename)
                logger.info(f"✅ {filename} uploadé")
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='STAGED' WHERE file_name=%s", (filename,))
                logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
            except Exception as e:
                logger.error(f"❌ Erreur upload {filename}: {e}")
                logger.debug(f"🚀 Chargement de {METADATA_TABLE}")
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='FAILED_STAGE' WHERE file_name=%s", (filename,))
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        shutil.rmtree("temp_files", ignore_errors=True)
    conn.close()

if __name__ == "__main__":
    main()
