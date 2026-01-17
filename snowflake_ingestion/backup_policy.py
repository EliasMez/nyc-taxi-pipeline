from snowflake.connector.cursor import SnowflakeCursor
import snowflake_ingestion.functions as functions

functions.config_logger()
logger = functions.logging.getLogger(__name__)

SQL_DIR = functions.SQL_BASE_DIR / "backup"


def create_and_set_backup(cur: SnowflakeCursor) -> None:
    """Creates the backup policies and backup sets for the data warehouse.

    Executes the SQL script to create the monthly backup policies and
    link them to the target objects (full database, raw table, final schema).

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("🔐 Creating backup policies and sets...")
    sql_file = SQL_DIR / "create_and_set_backup.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info(f"✅ {functions.DW_NAME}_BACKUP retention : {functions.FULL_BACKUP_POLICY_DAYS}")
    logger.info(f"✅ {functions.RAW_TABLE}_BACKUP retention : {functions.RAW_TABLE_BACKUP_POLICY_DAYS}")
    logger.info(f"✅ {functions.FINAL_SCHEMA}_BACKUP retention : {functions.FINAL_SCHEMA_BACKUP_POLICY_DAYS}")

def main() -> None:
    """Main initialization process for the Snowflake environment.

    Establishes connections with appropriate roles (SYSADMIN, SECURITYADMIN, ACCOUNTADMIN)
    and executes setup steps in order.
    """
    try:
        conn = functions.connect_with_role(functions.USER, functions.PASSWORD, functions.ACCOUNT, "SYSADMIN")
        with conn.cursor() as cur:
            create_and_set_backup(cur)
        conn.close()


        logger.info("🎯 Complete initialization finished successfully!")
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    main()