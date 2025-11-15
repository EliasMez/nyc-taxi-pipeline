import snowflake.connector
import os
import sys
import logging
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
USER = os.getenv('SNOWFLAKE_USER')
PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
PASSWORD_DEV = os.getenv('PASSWORD_DEV')

WH_NAME = os.getenv('WH_NAME')
DW_NAME = os.getenv('DW_NAME')
RAW_SCHEMA = os.getenv('RAW_SCHEMA')
RAW_TABLE = os.getenv('RAW_TABLE')
METADATA_TABLE = os.getenv('METADATA_TABLE')

PARQUET_FORMAT = os.getenv('PARQUET_FORMAT')
ROLE_TRANSFORMER = os.getenv('ROLE_TRANSFORMER')
USER_DEV = os.getenv('USER_DEV')

SCRAPING_YEAR = os.getenv('SCRAPING_YEAR')
LOGGER_LEVEL = getattr(logging, os.getenv('LOGGER_LEVEL'))


SQL_BASE_DIR = Path("snowflake_ingestion") / "sql"



def config_logger():
    """Configure the global logger.

    Reads LOGGER_LEVEL from the module environment and configures the
    root logging settings (level, format, date format). Intended to be
    called once at application start.

    No return value.
    """
    logging.basicConfig(
        level=LOGGER_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

config_logger()
logger = logging.getLogger(__name__)



def connect_with_role(user, password, account, role):
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
        autocommit=True
    )


def use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA):
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
    try :
        cur.execute(f"USE WAREHOUSE {WH_NAME}")
        cur.execute(f"USE DATABASE {DW_NAME}")
        cur.execute(f"USE SCHEMA {RAW_SCHEMA}")
    except Exception as e:
        logger.critical(f"❌ Erreur : Relancer l'étape 01 - Initialisation")
        sys.exit(1)



def run_sql_file(cur, filepath):
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
        a string of the form "<VAR_NOT_FOUND>".
    """
    with open(filepath, "r") as f:
        sql = f.read()
        keys = re.findall(r"(\w+)_PLACEHOLDER", sql)
        variables = {k: globals().get(k, f"<{k}_NOT_FOUND>") for k in keys}
        logger.debug(f"🔎 Variables détectées dans {filepath.name}: {sorted(set(keys))}")
        for key, value in variables.items():
            sql = sql.replace(f"{key}_PLACEHOLDER", str(value))
        
        masked_vars = {k: "*****" if "PASSWORD" in k.upper() else v for k, v in variables.items()}
        logger.debug(f"🧱 Variables utilisées : {dict(sorted(masked_vars.items()))}")

        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                cur.execute(statement)
