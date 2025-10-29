import snowflake.connector
import os
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



def connect_with_role(user, password, account, role):
    """Crée une connexion Snowflake avec le rôle spécifié."""
    return snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        role=role,
        autocommit=True
    )


def use_context(cur, WH_NAME, DW_NAME, RAW_SCHEMA):
    cur.execute(f"USE WAREHOUSE {WH_NAME}")
    cur.execute(f"USE DATABASE {DW_NAME}")
    cur.execute(f"USE SCHEMA {RAW_SCHEMA}")