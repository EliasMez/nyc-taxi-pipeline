from functions import connect_with_role
from functions import ACCOUNT, USER, PASSWORD
from functions import WH_NAME, DW_NAME, RAW_SCHEMA, PARQUET_FORMAT
from functions import ROLE_TRANSFORMER, USER_DEV, PASSWORD_DEV
from functions import config_logger
import logging

config_logger()
logger = logging.getLogger(__name__)

# -------------------------------------------------------
# 1️⃣ Étape 1 : Création du warehouse, DB et schémas (SYSADMIN)
# -------------------------------------------------------
def setup_data_warehouse():
    logger.info("🏗️ Création du warehouse, base et schémas...")
    conn = connect_with_role(USER, PASSWORD, ACCOUNT, 'SYSADMIN')
    with conn.cursor() as cur:

        cur.execute(f"""
            CREATE WAREHOUSE IF NOT EXISTS {WH_NAME}
            WITH WAREHOUSE_SIZE = 'X-SMALL'
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
        """)

        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DW_NAME}")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {DW_NAME}.{RAW_SCHEMA}")

        # Création du format Parquet dans RAW
        cur.execute(f"CREATE FILE FORMAT IF NOT EXISTS {DW_NAME}.{RAW_SCHEMA}.{PARQUET_FORMAT} TYPE='PARQUET'")

        logger.info("✅ Warehouse, DB et schémas créés avec succès")
    conn.close()


# -------------------------------------------------------
# 2️⃣ Étape 2 : Création du rôle et de l’utilisateur DBT (SECURITYADMIN)
# -------------------------------------------------------
def create_roles_and_user():
    logger.info("🔐 Création du rôle et de l'utilisateur DBT...")
    conn = connect_with_role(USER, PASSWORD, ACCOUNT, 'SECURITYADMIN')
    with conn.cursor() as cur:
        cur.execute(f"USE ROLE SECURITYADMIN")

        # Création du rôle
        cur.execute(f"CREATE ROLE IF NOT EXISTS {ROLE_TRANSFORMER}")

        # Création de l'utilisateur DBT
        cur.execute(f"""
            CREATE USER IF NOT EXISTS {USER_DEV} 
            PASSWORD='{PASSWORD_DEV}'
            LOGIN_NAME='{USER_DEV}'
            MUST_CHANGE_PASSWORD=FALSE
            DEFAULT_WAREHOUSE='{WH_NAME}'
            DEFAULT_ROLE='{ROLE_TRANSFORMER}'
            DEFAULT_NAMESPACE='{DW_NAME}.{RAW_SCHEMA}'
            COMMENT='Utilisateur Snowflake pour ingestion et transformations DBT';
        """)

        # Attribution du rôle à l’utilisateur et au SYSADMIN pour gestion
        cur.execute(f"GRANT ROLE {ROLE_TRANSFORMER} TO USER {USER_DEV}")
        cur.execute(f"GRANT ROLE {ROLE_TRANSFORMER} TO ROLE SYSADMIN")

        logger.info("✅ Rôle et utilisateur DBT créés avec succès")
    conn.close()


# -------------------------------------------------------
# 3️⃣ Étape 3 : Attribution des privilèges au rôle TRANSFORMER (SYSADMIN)
# -------------------------------------------------------
def grant_privileges():
    logger.info("🔑 Attribution des privilèges au rôle TRANSFORMER...")
    conn = connect_with_role(USER, PASSWORD, ACCOUNT, 'SYSADMIN')
    with conn.cursor() as cur:
        cur.execute(f"USE ROLE SYSADMIN")

        # Droits sur le warehouse
        cur.execute(f"GRANT ALL ON WAREHOUSE {WH_NAME} TO ROLE {ROLE_TRANSFORMER}")

        # Droits sur la database
        cur.execute(f"GRANT ALL ON DATABASE {DW_NAME} TO ROLE {ROLE_TRANSFORMER}")

        # Droits sur tous les schémas existants et futurs
        cur.execute(f"GRANT ALL ON ALL SCHEMAS IN DATABASE {DW_NAME} TO ROLE {ROLE_TRANSFORMER}")
        cur.execute(f"GRANT ALL ON FUTURE SCHEMAS IN DATABASE {DW_NAME} TO ROLE {ROLE_TRANSFORMER}")

        # Droits sur toutes les tables existantes et futures du schéma RAW
        cur.execute(f"GRANT ALL ON ALL TABLES IN SCHEMA {DW_NAME}.{RAW_SCHEMA} TO ROLE {ROLE_TRANSFORMER}")
        cur.execute(f"GRANT ALL ON FUTURE TABLES IN SCHEMA {DW_NAME}.{RAW_SCHEMA} TO ROLE {ROLE_TRANSFORMER}")

        # Droits sur le file format existant du schéma RAW
        cur.execute(f"GRANT USAGE ON FILE FORMAT {DW_NAME}.{RAW_SCHEMA}.{PARQUET_FORMAT} TO ROLE {ROLE_TRANSFORMER}")

        logger.info("✅ Privilèges attribués avec succès")
    conn.close()


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
def main():
    try:
        setup_data_warehouse()
        create_roles_and_user()
        grant_privileges()
        logger.info("🎯 Initialisation complète terminée avec succès !")
    except Exception as e:
        logger.error(f"❌ Erreur : {e}")


if __name__ == "__main__":
    main()
