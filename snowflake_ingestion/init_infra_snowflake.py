import snowflake_ingestion.functions as functions
functions.config_logger()
logger = functions.logging.getLogger(__name__)


SQL_DIR = functions.SQL_BASE_DIR / "init"



def setup_data_warehouse(cur):
    """Create the data warehouse, database, and schemas in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🏗️  Création du warehouse, base et schémas...")
    sql_file = SQL_DIR / "setup_data_warehouse.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Warehouse et schémas créés")


def create_roles_and_user(cur):
    """Create the DBT role and user in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🔐 Création du rôle et de l'utilisateur DBT...")
    sql_file = SQL_DIR / "create_roles_and_user.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Rôle et utilisateur créés")


def grant_privileges(cur):
    """Grant required privileges to the TRANSFORMER role in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🔑 Attribution des privilèges au rôle TRANSFORMER...")
    sql_file = SQL_DIR / "grant_privileges.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Privilèges attribués")


def main():
    """Main initialization process for the Snowflake environment.

    Establishes connections with appropriate roles (SYSADMIN, SECURITYADMIN)
    and executes setup steps in order.
    """
    try:
        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, 'SYSADMIN')
        with conn.cursor() as cur:
            setup_data_warehouse(cur)
        conn.close()

        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, 'SECURITYADMIN')
        with conn.cursor() as cur:
            create_roles_and_user(cur)
            grant_privileges(cur)
        conn.close()

        logger.info("🎯 Initialisation complète terminée avec succès !")
    except Exception as e:
        logger.error(f"❌ Erreur : {e}")

if __name__ == "__main__":
    main()
