import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.backup_policy as backup

def test_create_and_set_backup():
    """
    Test the create_and_set_backup function execution.
    
    Verifies that the function runs the correct SQL file and logs appropriate
    messages with retention period information for each backup policy.
    """
    mock_cursor = Mock()
    
    with patch('snowflake_ingestion.backup_policy.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.backup_policy.logger') as mock_logger:
            with patch('snowflake_ingestion.backup_policy.functions.DW_NAME', 'TEST_DW'):
                with patch('snowflake_ingestion.backup_policy.functions.RAW_TABLE', 'TEST_RAW'):
                    with patch('snowflake_ingestion.backup_policy.functions.FINAL_SCHEMA', 'TEST_FINAL'):
                        with patch('snowflake_ingestion.backup_policy.functions.FULL_BACKUP_POLICY_DAYS', 90):
                            with patch('snowflake_ingestion.backup_policy.functions.RAW_TABLE_BACKUP_POLICY_DAYS', 180):
                                with patch('snowflake_ingestion.backup_policy.functions.FINAL_SCHEMA_BACKUP_POLICY_DAYS', 365):
                                    
                                    backup.create_and_set_backup(mock_cursor)
                                    
                                    expected_sql_file = backup.SQL_DIR / "create_and_set_backup.sql"
                                    mock_run_sql.assert_called_once_with(mock_cursor, expected_sql_file)
                                    
                                    mock_logger.info.assert_any_call("🔐 Creating backup policies and sets...")
                                    mock_logger.info.assert_any_call("✅ TEST_DW_BACKUP retention : 90")
                                    mock_logger.info.assert_any_call("✅ TEST_RAW_BACKUP retention : 180")
                                    mock_logger.info.assert_any_call("✅ TEST_FINAL_BACKUP retention : 365")

def test_main_success():
    """
    Test the main function with successful backup setup workflow.
    
    Ensures connection is made with SYSADMIN role, backup function is called,
    connection is closed properly, and success is logged.
    """
    mock_conn = Mock()
    mock_cursor = Mock()
    
    mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = Mock(return_value=None)
    
    with patch('snowflake_ingestion.backup_policy.functions.connect_with_role', return_value=mock_conn) as mock_connect:
        with patch('snowflake_ingestion.backup_policy.create_and_set_backup') as mock_create_backup:
            with patch('snowflake_ingestion.backup_policy.logger') as mock_logger:
                
                backup.main()
                
                mock_connect.assert_called_once_with(
                    backup.functions.USER,
                    backup.functions.PASSWORD,
                    backup.functions.ACCOUNT,
                    "SYSADMIN"
                )
                
                mock_create_backup.assert_called_once_with(mock_cursor)
                mock_conn.close.assert_called_once()
                mock_logger.info.assert_called_with("🎯 Complete initialization finished successfully!")

def test_main_exception():
    """
    Test error handling in main function when an exception occurs.
    
    Verifies that exceptions are caught and logged as errors without crashing.
    """
    test_exception = Exception("Connection failed: Invalid credentials")
    
    with patch('snowflake_ingestion.backup_policy.functions.connect_with_role', side_effect=test_exception):
        with patch('snowflake_ingestion.backup_policy.logger') as mock_logger:
            
            backup.main()
            mock_logger.error.assert_called_once_with(test_exception)

def test_main_with_connection_context():
    """
    Test proper cursor context management in main function.
    
    Verifies that cursor context manager protocols are followed correctly.
    """
    mock_conn = Mock()
    mock_cursor_context = Mock()
    mock_cursor = Mock()
    
    mock_cursor_context.__enter__ = Mock(return_value=mock_cursor)
    mock_cursor_context.__exit__ = Mock(return_value=None)
    mock_conn.cursor.return_value = mock_cursor_context
    
    with patch('snowflake_ingestion.backup_policy.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.backup_policy.create_and_set_backup'):
            with patch('snowflake_ingestion.backup_policy.logger'):
                
                backup.main()
                mock_conn.cursor.assert_called_once()
                mock_cursor_context.__enter__.assert_called_once()
                mock_cursor_context.__exit__.assert_called_once()

def test_backup_configuration_values():
    """
    Test backup configuration constants are properly accessed and logged.
    
    Ensures retention days for different backup policies are correctly
    formatted in log messages.
    """
    mock_cursor = Mock()
    
    with patch('snowflake_ingestion.backup_policy.functions.run_sql_file'):
        with patch('snowflake_ingestion.backup_policy.logger') as mock_logger:
            with patch('snowflake_ingestion.backup_policy.functions.DW_NAME', 'PRODUCTION_DW'):
                with patch('snowflake_ingestion.backup_policy.functions.RAW_TABLE', 'YELLOW_TAXI'):
                    with patch('snowflake_ingestion.backup_policy.functions.FINAL_SCHEMA', 'ANALYTICS'):
                        with patch('snowflake_ingestion.backup_policy.functions.FULL_BACKUP_POLICY_DAYS', 365):
                            with patch('snowflake_ingestion.backup_policy.functions.RAW_TABLE_BACKUP_POLICY_DAYS', 730):
                                with patch('snowflake_ingestion.backup_policy.functions.FINAL_SCHEMA_BACKUP_POLICY_DAYS', 180):
                                    
                                    backup.create_and_set_backup(mock_cursor)
                                    
                                    mock_logger.info.assert_any_call("✅ PRODUCTION_DW_BACKUP retention : 365")
                                    mock_logger.info.assert_any_call("✅ YELLOW_TAXI_BACKUP retention : 730")
                                    mock_logger.info.assert_any_call("✅ ANALYTICS_BACKUP retention : 180")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])