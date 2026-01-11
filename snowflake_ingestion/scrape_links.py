from typing import List
from datetime import datetime
import requests
from lxml import html
from snowflake.connector.cursor import SnowflakeCursor
import snowflake_ingestion.functions as functions

functions.config_logger()
logger = functions.logging.getLogger(__name__)

SQL_DIR = functions.SQL_BASE_DIR / "scraping"
current_year: int = datetime.now().year
current_month: int = datetime.now().month
scraping_url: str = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"

def get_scraping_year() -> int:
    """Determine the scraping year to use based on environment settings.
    Uses SCRAPING_YEAR if defined and valid, otherwise selects the previous
    year when current month ≤ 3, or the current year otherwise.

    Returns:
        int: The year to scrape.

    Doctests:
    from functions import SCRAPING_YEAR
    >>> get_scraping_year() == (int(SCRAPING_YEAR) if SCRAPING_YEAR != '' else current_year) - int(current_month <= 3)
    True

    """
    default_year = current_year - 1 if current_month <= 3 else current_year
    if functions.SCRAPING_YEAR == "":
        return default_year
    else:
        try:
            int_year = int(functions.SCRAPING_YEAR)
        except ValueError:
            logger.error(f"\"SCRAPING_YEAR = {functions.SCRAPING_YEAR}\" is not a valid year!")
            logger.warning(f"Scraping year has been reset to {default_year}")
            return default_year

        if int_year < 2009 or int_year > current_year:
            logger.error(
                f"\"SCRAPING_YEAR = {functions.SCRAPING_YEAR}\" scraping year must be between 2009 and {current_year} inclusive!"
            )
            logger.warning(f"Scraping year has been reset to {default_year}")
            return default_year
        logger.info(f"Files will be scraped from year {default_year}")
        return int_year

def get_xpath() -> str:
    """Build the XPath expression used to locate Parquet file links.
    The expression filters NYC Taxi data links by year, starting from the
    scraping year up to the current year.

    Returns:
        str: XPath query string.
    """
    xpath_query = "//a[@title='Yellow Taxi Trip Records' and ("
    get_contains = lambda year: f"contains(@href, '{year}')"
    contains_list = [get_contains(year) for year in range(get_scraping_year(), current_year + 1)]
    xpath_query += " or ".join(contains_list) + ")]"
    return xpath_query

def get_parquet_links() -> List[str]:
    """Scrape the NYC Taxi data page for Parquet file URLs.
    Sends an HTTP request to the NYC Taxi,parses the page HTML,
    and extracts links to Parquet files for the relevant years.

    Returns:
        list[str]: List of Parquet file URLs.
    """
    logger.info("🌐 Starting NYC Taxi data scraping")
    response = requests.get(scraping_url)
    tree = html.fromstring(response.content)
    xpath_query = get_xpath()
    filtered_links = tree.xpath(xpath_query)
    return [
        link.get("href")
        for link in filtered_links
        if link.get("href") and link.get("href").endswith(".parquet")
    ]

def setup_meta_table(cur: SnowflakeCursor) -> None:
    """Ensure the metadata table exists in Snowflake.
    Executes the SQL script responsible for creating or verifying the
    metadata table.

    Args:
        cur (snowflake.connector.cursor.SnowflakeCursor): Active Snowflake cursor.
    """
    logger.info("📋 Verification/Creation of metadata table")
    sql_file = SQL_DIR / "setup_meta_table.sql"
    functions.run_sql_file(cur, sql_file)
    logger.info("✅ Metadata table ready")

def main() -> None:
    """Main scraping and metadata update workflow.
    Connects to Snowflake using the transformer role, initializes context,
    checks or creates the metadata table, scrapes new file URLs, and updates
    the metadata accordingly.
    """
    conn = functions.connect_with_role(
        functions.USER_DEV,
        functions.PASSWORD_DEV,
        functions.ACCOUNT,
        functions.ROLE_TRANSFORMER,
    )
    with conn.cursor() as cur:
        functions.use_context(cur, functions.WH_NAME, functions.DW_NAME, functions.RAW_SCHEMA)
        setup_meta_table(cur)

        links = get_parquet_links()
        s = functions.plural_suffix(len(links))
        logger.info(f"📎 {len(links)} link{s} found")
        new_file_detected: bool = False

        for url in links:
            filename = url.split("/")[-1]
            cur.execute(
                f"SELECT 1 FROM {functions.METADATA_TABLE} WHERE file_name = %s",
                (filename,),
            )
            if not cur.fetchone():
                logger.info(f"➕ New file detected : {filename}")
                new_file_detected = True

                parts = (
                    filename.replace("yellow_tripdata_", "")
                    .replace(".parquet", "")
                    .split("-")
                )
                year = int(parts[0]) if len(parts) > 0 else None
                month = int(parts[1]) if len(parts) > 1 else None

                logger.debug(f"🚀 Loading {functions.METADATA_TABLE}")
                cur.execute(
                    f"""
                    INSERT INTO {functions.METADATA_TABLE}
                    (file_url, file_name, year, month, rows_loaded, load_status)
                    VALUES (%s, %s, %s, %s, 0, 'SCRAPED')
                    """,
                    (url, filename, year, month),
                )
            else:
                logger.info(f"⏭️  {filename} already referenced")

            if not new_file_detected:
                logger.debug("🔍 Analyzing SCRAPED files")
                functions.run_sql_file(cur, SQL_DIR / "count_new_files.sql")
                if cur.fetchone()[0] > 0:
                    new_file_detected = True

    conn.close()

    if not new_file_detected:
        logger.warning("⚠️  No new files to load.")

    logger.info("✅ Scraping completed")

if __name__ == "__main__":
    if functions.LOGGER_LEVEL == "DEBUG":
        import doctest
        doctest.testmod(verbose=True)
    main()