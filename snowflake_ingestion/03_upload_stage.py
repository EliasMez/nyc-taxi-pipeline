import os
import requests
import shutil
from functions import connect_with_role, use_context
from functions import ACCOUNT
from functions import WH_NAME, DW_NAME, RAW_SCHEMA, METADATA_TABLE
from functions import ROLE_TRANSFORMER, USER_DEV, PASSWORD_DEV
from functions import config_logger
import logging

config_logger()
logger = logging.getLogger(__name__)

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
        cur.execute(f"SELECT file_url, file_name FROM {METADATA_TABLE} WHERE load_status='SCRAPED'")
        scraped_files = cur.fetchall()
        logger.info(f"📦 {len(scraped_files)} fichiers à uploader")

        for file_url, filename in scraped_files:
            try:
                tmp_path = download_and_upload_file(cur, file_url, filename)
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='STAGED' WHERE file_name=%s", (filename,))
                logger.info(f"✅ {filename} uploadé")
            except Exception as e:
                logger.error(f"❌ Erreur upload {filename}: {e}")
                cur.execute(f"UPDATE {METADATA_TABLE} SET load_status='FAILED_STAGE' WHERE file_name=%s", (filename,))
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
        shutil.rmtree("temp_files", ignore_errors=True)
    conn.close()

if __name__ == "__main__":
    main()
