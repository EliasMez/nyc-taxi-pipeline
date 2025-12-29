import snowflake.connector
import os
import sys
import logging
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ACCOUNT: str = os.getenv("SNOWFLAKE_ACCOUNT")
USER: str = os.getenv("SNOWFLAKE_USER")
PASSWORD: str = os.getenv("SNOWFLAKE_PASSWORD")

WH_NAME: str = os.getenv("WH_NAME")
DW_NAME: str = os.getenv("DW_NAME")

RAW_SCHEMA: str = os.getenv("RAW_SCHEMA")
STAGING_SCHEMA: str = os.getenv("STAGING_SCHEMA")
FINAL_SCHEMA: str = os.getenv("FINAL_SCHEMA")

RAW_TABLE: str = os.getenv("RAW_TABLE")
METADATA_TABLE: str = os.getenv("METADATA_TABLE")

PARQUET_FORMAT: str = os.getenv("PARQUET_FORMAT")
ID_SEQUENCE: str = os.getenv("ID_SEQUENCE")
COMPUTE_SIZE: str = os.getenv("COMPUTE_SIZE")

ROLE_TRANSFORMER: str = os.getenv("ROLE_TRANSFORMER")
ROLE_BI_ANALYST: str = os.getenv("ROLE_BI_ANALYST")
ROLE_DATA_SCIENTIST: str = os.getenv("ROLE_DATA_SCIENTIST")
ROLE_MART_CONSUMER: str = os.getenv("ROLE_MART_CONSUMER")

USER_DEV: str = os.getenv("USER_DEV")
USER_BI_ANALYST: str = os.getenv("USER_BI_ANALYST")
USER_DATA_SCIENTIST: str = os.getenv("USER_DATA_SCIENTIST")
USER_MART_CONSUMER: str = os.getenv("USER_MART_CONSUMER")

PASSWORD_DEV: str = os.getenv("PASSWORD_DEV")
PASSWORD_BI: str = os.getenv("PASSWORD_BI")
PASSWORD_DS: str = os.getenv("PASSWORD_DS")
PASSWORD_MC: str = os.getenv("PASSWORD_MC")

SCRAPING_YEAR: str = os.getenv("SCRAPING_YEAR")
TIMEZONE: str = os.getenv("TIMEZONE")
LOGGER_LEVEL: int = getattr(logging, os.getenv("LOGGER_LEVEL"))

SQL_BASE_DIR: Path = Path("snowflake_ingestion") / "sql"

def config_logger() -> None:
    """Configure the global logger.

    Reads LOGGER_LEVEL from the module environment and configures the
    root logging settings (level, format, date format). Intended to be
    called once at application start.

    No return value.
    """
    logging.basicConfig(
        level=LOGGER_LEVEL,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

config_logger()
logger: logging.Logger = logging.getLogger(__name__)

def connect_with_role(user: str, password: str, account: str, role: str) -> snowflake.connector.SnowflakeConnection:
    """Create a Snowflake connection using the specified credentials and role.

    Args:
        user (str): Snowflake username.
        password (str): Snowflake password.
        account (str): Snowflake account identifier.
        role (str): Snowflake role to assume for the session.

    Returns:
        snowflake.connector.connection.SnowflakeConnection:
            A Snowflake connection object with autocommit enabled.

    Notes:
        This function opens a network connection to Snowflake. The caller
        is responsible for closing the connection when it is no longer needed.
    """
    return snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        role=role,
        autocommit=True,
    )

def use_context(cur: snowflake.connector.cursor.SnowflakeCursor, WH_NAME: str, DW_NAME: str, RAW_SCHEMA: str) -> None:
    """Set the Snowflake session context: warehouse, database and schema.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
        WH_NAME (str): Warehouse name to use.
        DW_NAME (str): Database name to use.
        RAW_SCHEMA (str): Schema name to use.

    Raises:
        SystemExit: Exits the process on any exception when setting the context.
    """
    logger.debug(f"⚙️ Configuration du contexte: WH={WH_NAME}, DB={DW_NAME}, SCHEMA={RAW_SCHEMA}")
    try:
        cur.execute(f"USE WAREHOUSE {WH_NAME}")
        cur.execute(f"USE DATABASE {DW_NAME}")
        cur.execute(f"USE SCHEMA {RAW_SCHEMA}")
    except Exception as e:
        logger.critical("❌ Erreur : Relancer l'étape Snowflake Infra Init")
        sys.exit(1)


def run_sql_file(cur: snowflake.connector.cursor.SnowflakeCursor, filepath: Path | str) -> None:
    """Execute SQL statements from a file using VAR_PLACEHOLDER placeholders.

    The function:
      - Reads the SQL file.
      - Finds placeholders in the form VAR_PLACEHOLDER (captures VAR).
      - Replaces each found placeholder with the value of the corresponding
        global variable named VAR (stringified).
      - Masks variables containing "PASSWORD" in logger output.
      - Splits the file by semicolons and executes non-empty statements.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active cursor.
        filepath (pathlib.Path or str): Path to the SQL file.

    Notes:
        Placeholders that do not match a global variable are replaced with
        a string of the form `<VAR_NOT_FOUND>`.
    """
    with open(filepath, "r") as f:
        sql = f.read()
        keys = re.findall(r'(?:SCHEMA_)?(\w+)_PLACEHOLDER', sql)
        variables = {k: globals().get(k, f"<{k}_NOT_FOUND>") for k in keys}
        logger.debug(f"🔎 Variables détectées dans {Path(filepath).name}: {sorted(set(keys))}")
        for key, value in variables.items():
            sql = sql.replace(f"{key}_PLACEHOLDER", str(value))
        masked_vars = {k: "*****" if "PASSWORD" in k.upper() else v for k, v in variables.items()}
        logger.debug(f"Variables utilisées : {dict(sorted(masked_vars.items()))}")

        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                cur.execute(statement)
