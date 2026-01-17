import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.scrape_links as scrape

def test_get_scraping_year_with_valid_env():
    """
    Test that get_scraping_year correctly parses and returns a valid integer value from the SCRAPING_YEAR environment variable.
    Verifies that when SCRAPING_YEAR is set to '2023', the function returns the integer 2023.
    """
    with patch('snowflake_ingestion.scrape_links.functions.SCRAPING_YEAR', '2023'):
        result = scrape.get_scraping_year()
        assert result == 2023

def test_get_scraping_year_with_empty_env_early_month():
    """
    Test get_scraping_year behavior when SCRAPING_YEAR is empty and current month is early (January to March).
    The function should default to the previous year since current year's data may not be fully available yet.
    """
    with patch('snowflake_ingestion.scrape_links.functions.SCRAPING_YEAR', ''):
        with patch('snowflake_ingestion.scrape_links.current_month', 1):
            result = scrape.get_scraping_year()
            expected = scrape.current_year - 1
            assert result == expected

def test_get_scraping_year_with_empty_env_late_month():
    """
    Test get_scraping_year behavior when SCRAPING_YEAR is empty and current month is late (April to December).
    The function should default to the current year for scraping operations.
    """
    with patch('snowflake_ingestion.scrape_links.functions.SCRAPING_YEAR', ''):
        with patch('snowflake_ingestion.scrape_links.current_month', 4):
            result = scrape.get_scraping_year()
            expected = scrape.current_year
            assert result == expected

def test_get_scraping_year_with_invalid_env_early_month():
    """
    Test get_scraping_year behavior when SCRAPING_YEAR contains invalid non-numeric data in early months.
    The function should log an error and default to the previous year while handling the invalid input gracefully.
    """
    with patch('snowflake_ingestion.scrape_links.functions.SCRAPING_YEAR', 'invalid'):
        with patch('snowflake_ingestion.scrape_links.current_month', 3):
            with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                result = scrape.get_scraping_year()
                expected = scrape.current_year - 1
                assert result == expected
                mock_logger.error.assert_called_once()

def test_get_scraping_year_with_invalid_env_late_month():
    """
    Test get_scraping_year behavior when SCRAPING_YEAR contains invalid non-numeric data in late months.
    The function should log an error and default to the current year while handling the invalid input gracefully.
    """
    with patch('snowflake_ingestion.scrape_links.functions.SCRAPING_YEAR', 'invalid'):
        with patch('snowflake_ingestion.scrape_links.current_month', 12):
            with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                result = scrape.get_scraping_year()
                expected = scrape.current_year
                assert result == expected
                mock_logger.error.assert_called_once()

def test_get_xpath():
    """
    Test that get_xpath generates the correct XPath expression for locating Yellow Taxi Trip Records links.
    The XPath should include both the scraping year and current year to capture relevant data files.
    """
    with patch('snowflake_ingestion.scrape_links.get_scraping_year', return_value=2023):
        with patch('snowflake_ingestion.scrape_links.current_year', 2024):
            result = scrape.get_xpath()
            expected = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2023') or contains(@href, '2024'))]"
            assert result == expected

def test_get_parquet_links_success():
    """
    Test successful extraction of parquet file links from the NYC TLC website HTML content.
    Verifies that only links with title 'Yellow Taxi Trip Records' are extracted and returned.
    """
    mock_html_content = """
    <html>
        <a title="Yellow Taxi Trip Records" href="https://example.com/file1.parquet">Link1</a>
        <a title="Yellow Taxi Trip Records" href="https://example.com/file2.parquet">Link2</a>
        <a title="Other Title" href="https://example.com/file3.parquet">Link3</a>
    </html>
    """
    mock_response = Mock()
    mock_response.content = mock_html_content.encode()

    mock_tree = Mock()
    mock_link1 = Mock()
    mock_link1.get.return_value = "https://example.com/file1.parquet"
    mock_link2 = Mock()
    mock_link2.get.return_value = "https://example.com/file2.parquet"
    mock_tree.xpath.return_value = [mock_link1, mock_link2]
    
    with patch('snowflake_ingestion.scrape_links.requests.get') as mock_get:
        with patch('snowflake_ingestion.scrape_links.html.fromstring') as mock_fromstring:
            with patch('snowflake_ingestion.scrape_links.get_xpath', return_value="//a[@title='Yellow Taxi Trip Records']"):
                with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                    mock_get.return_value = mock_response
                    mock_fromstring.return_value = mock_tree
                    
                    result = scrape.get_parquet_links()

                    mock_get.assert_called_once_with("https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
                    mock_logger.info.assert_called_with("🌐 Starting NYC Taxi data scraping")
                    assert result == ["https://example.com/file1.parquet", "https://example.com/file2.parquet"]

def test_setup_meta_table():
    """
    Test that setup_meta_table correctly executes the SQL script for creating or verifying the metadata table.
    Verifies that the appropriate SQL file is executed and success/failure logs are recorded.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.scrape_links.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
            scrape.setup_meta_table(mock_cursor)
            mock_run_sql.assert_called_once_with(mock_cursor, scrape.SQL_DIR / "setup_meta_table.sql")
            mock_logger.info.assert_any_call("📋 Verification/Creation of metadata table")
            mock_logger.info.assert_any_call("✅ Metadata table ready")

def test_main_with_new_files():
    """
    Test the main scraping workflow when new parquet files are detected that don't exist in the metadata table.
    Verifies that new files trigger INSERT operations into the metadata table with appropriate logging.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, None, [5]]
    
    with patch('snowflake_ingestion.scrape_links.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.functions.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.functions.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                            
                            mock_links.return_value = [
                                "https://example.com/yellow_tripdata_2023-01.parquet",
                                "https://example.com/yellow_tripdata_2023-02.parquet"
                            ]
                            
                            scrape.main()

                            assert mock_cursor.execute.call_count >= 4
                            mock_logger.info.assert_any_call("📎 2 links found")
                            mock_logger.info.assert_any_call("➕ New file detected : yellow_tripdata_2023-01.parquet")

def test_main_without_new_files():
    """
    Test the main scraping workflow when all discovered parquet files already exist in the metadata table.
    Verifies that no INSERT operations occur and appropriate informational and warning logs are recorded.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [[1], [0]]
    
    with patch('snowflake_ingestion.scrape_links.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.functions.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.functions.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                            mock_links.return_value = ["https://example.com/yellow_tripdata_2023-01.parquet"]
                            scrape.main()
                            mock_logger.info.assert_any_call("📎 1 link found")
                            mock_logger.info.assert_any_call("⏭️  yellow_tripdata_2023-01.parquet already referenced")
                            mock_logger.info.assert_any_call("✅ Scraping completed")
                            mock_logger.warning.assert_called_with("⚠️  No new files to load.")

def test_main_file_parsing():
    """
    Test that the main function correctly parses filename patterns to extract year and month components.
    Verifies that URLs like 'yellow_tripdata_2023-07.parquet' are correctly parsed into (2023, 7) tuples.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    with patch('snowflake_ingestion.scrape_links.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.functions.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.functions.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger'):
                            mock_links.return_value = ["https://example.com/yellow_tripdata_2023-07.parquet"]
                            scrape.main()
                            
                            insert_call = None
                            for call in mock_cursor.execute.call_args_list:
                                if 'INSERT' in str(call[0][0]):
                                    insert_call = call
                                    break
                            
                            assert insert_call is not None
                            assert insert_call[0][1] == ("https://example.com/yellow_tripdata_2023-07.parquet", 
                                                        "yellow_tripdata_2023-07.parquet", 2023, 7)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])