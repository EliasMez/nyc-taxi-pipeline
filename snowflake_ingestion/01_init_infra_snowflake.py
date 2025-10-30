from functions import *

config_logger()
logger = logging.getLogger(__name__)


SQL_DIR = SQL_BASE_DIR / "01_init"



def setup_data_warehouse(cur):
    logger.info("🏗️ Création du warehouse, base et schémas...")
    sql_file = SQL_DIR / "setup_data_warehouse.sql"
    run_sql_file(cur, sql_file)
    logger.info("✅ Warehouse et schémas créés")


def create_roles_and_user(cur):
    logger.info("🔐 Création du rôle et de l'utilisateur DBT...")
    sql_file = SQL_DIR / "create_roles_and_user.sql"
    run_sql_file(cur, sql_file)
    logger.info("✅ Rôle et utilisateur créés")


def grant_privileges(cur):
    logger.info("🔑 Attribution des privilèges au rôle TRANSFORMER...")
    sql_file = SQL_DIR / "grant_privileges.sql"
    run_sql_file(cur, sql_file)
    logger.info("✅ Privilèges attribués")


def main():
    try:
        conn = connect_with_role(USER, PASSWORD, ACCOUNT, 'SYSADMIN')
        with conn.cursor() as cur:
            setup_data_warehouse(cur)
        conn.close()

        conn = connect_with_role(USER, PASSWORD, ACCOUNT, 'SECURITYADMIN')
        with conn.cursor() as cur:
            create_roles_and_user(cur)
            grant_privileges(cur)
        conn.close()

        logger.info("🎯 Initialisation complète terminée avec succès !")
    except Exception as e:
        logger.error(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
