from snowflake.connector.cursor import SnowflakeCursor
import snowflake_ingestion.functions as functions

functions.config_logger()
logger = functions.logging.getLogger(__name__)

SQL_DIR = functions.SQL_BASE_DIR / "init"


def set_data_retention(cur: SnowflakeCursor) -> None:
    """Set the data retention period for the Snowflake account.

    Checks if the account is Enterprise, then applies the retention time.
    Logs the result in days, with pluralization handled automatically.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🏗️  Setting up data retention")
    sql_file = SQL_DIR / "set_data_retention.sql"
    functions.run_sql_file(cur, sql_file)
    s = functions.plural_suffix(int(functions.RETENTION_TIME))
    logger.info(f"✅ Data retention set to {functions.RETENTION_TIME} day{s}")


def setup_data_warehouse(cur: SnowflakeCursor) -> None:
    """Create the data warehouse, database, and schemas in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🏗️  Creating warehouse, database and schemas...")
    sql_file = SQL_DIR / "setup_data_warehouse.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Warehouse and schemas created")

def create_roles_and_user(cur: SnowflakeCursor) -> None:
    """Create the DBT role and user in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🔐 Creating roles and users...")
    sql_file = SQL_DIR / "create_roles_and_user.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Roles and users created")

def grant_privileges(cur: SnowflakeCursor) -> None:
    """Grant required privileges to the TRANSFORMER role in Snowflake.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🔑 Granting privileges to the roles...")
    sql_file = SQL_DIR / "grant_privileges.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Privileges granted")

def main() -> None:
    """Main initialization process for the Snowflake environment.

    Establishes connections with appropriate roles (SYSADMIN, SECURITYADMIN, ACCOUNTADMIN)
    and executes setup steps in order.
    """
    try:
        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, "ACCOUNTADMIN")
        with conn.cursor() as cur:
            set_data_retention(cur)
        conn.close()

        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, "SYSADMIN")
        with conn.cursor() as cur:
            setup_data_warehouse(cur)
        conn.close()

        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, "SECURITYADMIN")
        with conn.cursor() as cur:
            create_roles_and_user(cur)
            grant_privileges(cur)
        conn.close()

        logger.info("🎯 Complete initialization finished successfully!")
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()