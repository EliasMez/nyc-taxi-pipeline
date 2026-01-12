import pytest
from unittest.mock import Mock, patch, MagicMock, ANY, call
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.load_to_table as load

def test_create_table_success():
    """Unit test for create_table with a valid schema."""
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        ("vendor_id", "NUMBER"),
        ("tpep_pickup_datetime", "TIMESTAMP_NTZ"),
        ("tpep_dropoff_datetime", "TIMESTAMP_NTZ")
    ]
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            result = load.create_table(mock_cursor)

            assert mock_run_sql.call_args_list[0] == call(mock_cursor, load.SQL_DIR / "detect_file_schema_stage.sql")
            assert mock_run_sql.call_args_list[1] == call(mock_cursor, load.SQL_DIR / "create_sequence.sql")
            assert mock_run_sql.call_args_list[2] == call(mock_cursor, load.SQL_DIR / "add_filename_to_raw_table.sql")
            
            mock_cursor.execute.assert_called_once()
            create_call = mock_cursor.execute.call_args[0][0]
            # CORRECTION : Ajout du mot "TRANSIENT"
            assert "CREATE TRANSIENT TABLE IF NOT EXISTS" in create_call
            assert "vendor_id NUMBER" in create_call
            assert "tpep_pickup_datetime TIMESTAMP_NTZ" in create_call
            
            mock_logger.info.assert_any_call(f"📋 Dynamic verification/creation of table {load.functions.RAW_TABLE}")
            mock_logger.info.assert_any_call(f"✅ Table {load.functions.RAW_TABLE} ready")
            
            assert result == [
                ("vendor_id", "NUMBER"),
                ("tpep_pickup_datetime", "TIMESTAMP_NTZ"),
                ("tpep_dropoff_datetime", "TIMESTAMP_NTZ")
            ]