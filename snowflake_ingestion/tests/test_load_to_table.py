import pytest
from unittest.mock import Mock, patch, MagicMock, ANY, call
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.load_to_table as load

def test_create_table_success():
    """Tests the successful creation of a table with dynamic schema detection.
    Verifies that all SQL files are executed in the correct order,
    the correct CREATE TABLE statement is generated, appropriate logs are recorded,
    and the correct table schema is returned.
    """
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        ("vendor_id", "NUMBER"),
        ("tpep_pickup_datetime", "TIMESTAMP_NTZ"),
        ("tpep_dropoff_datetime", "TIMESTAMP_NTZ")
    ]

    with patch('snowflake_ingestion.functions.run_sql_file') as mock_run_sql:
        # Correction: Patcher le logger dans le module load_to_table directement
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            result = load.create_table(mock_cursor)

            assert mock_run_sql.call_args_list[0] == call(mock_cursor, load.SQL_DIR / "detect_file_schema_stage.sql")
            assert mock_run_sql.call_args_list[1] == call(mock_cursor, load.SQL_DIR / "create_sequence.sql")
            assert mock_run_sql.call_args_list[2] == call(mock_cursor, load.SQL_DIR / "add_filename_to_raw_table.sql")

            mock_cursor.execute.assert_called_once()
            create_call = mock_cursor.execute.call_args[0][0]
            assert "CREATE TABLE IF NOT EXISTS" in create_call
            assert "vendor_id NUMBER" in create_call
            assert "tpep_pickup_datetime TIMESTAMP_NTZ" in create_call

            mock_logger.info.assert_any_call(f"📋 Dynamic verification/creation of table {load.functions.RAW_TABLE}")
            mock_logger.info.assert_any_call(f"✅ Table {load.functions.RAW_TABLE} ready")

            assert result == [
                ("vendor_id", "NUMBER"),
                ("tpep_pickup_datetime", "TIMESTAMP_NTZ"),
                ("tpep_dropoff_datetime", "TIMESTAMP_NTZ")
            ]

def test_create_table_no_schema():
    """Tests the behavior when the stage contains no data.
    Verifies that only the schema detection script runs, a warning is logged,
    no table creation SQL is executed, and an empty schema list is returned.
    """
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = []

    with patch('snowflake_ingestion.functions.run_sql_file') as mock_run_sql:
        # Correction: Patcher le logger dans le module load_to_table directement
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            result = load.create_table(mock_cursor)

            mock_run_sql.assert_called_once_with(mock_cursor, load.SQL_DIR / "detect_file_schema_stage.sql")
            mock_cursor.fetchall.assert_called_once()
            mock_logger.warning.assert_called_with("⚠️  No data in STAGE")
            mock_cursor.execute.assert_not_called()
            create_sequence_call = call(mock_cursor, load.SQL_DIR / "create_sequence.sql")
            add_filename_call = call(mock_cursor, load.SQL_DIR / "add_filename_to_raw_table.sql")
            assert create_sequence_call not in mock_run_sql.call_args_list
            assert add_filename_call not in mock_run_sql.call_args_list
            assert result == []

def test_copy_file_to_table_and_count_success():
    """Tests the successful execution of COPY INTO command.
    Verifies the command execution, correct parsing of the result,
    logging of success with row count, and the return of the correct number of loaded rows.
    """
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('test_file.parquet', 'LOADED', 250, 250, 1, 0, None, None, None, None)

    with patch('snowflake_ingestion.functions.run_sql_file'):
        # Correction: Patcher le logger dans le module load_to_table directement
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            table_schema = [("vendorid", "NUMBER"), ("tpep_pickup_datetime", "TIMESTAMP_NTZ")]
            result = load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet", table_schema)
            assert result == 250
            mock_cursor.execute.assert_called_once()
            mock_logger.info.assert_called_with("✅ test_file.parquet loaded (250 rows)")

def test_copy_file_to_table_and_count_zero_loaded():
    """Tests the COPY INTO command when no rows are processed.
    Verifies the function returns 0 when the execution result indicates no files were processed.
    """
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('Copy executed with 0 files processed.',)

    with patch('snowflake_ingestion.functions.run_sql_file'):
        # Correction: Patcher le logger dans le module load_to_table directement
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            table_schema = [("vendorid", "NUMBER"), ("tpep_pickup_datetime", "TIMESTAMP_NTZ")]
            result = load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet", table_schema)
            assert result == 0

def test_copy_file_to_table_and_count_copy_error():
    """Tests the handling of an exception raised during the COPY INTO execution.
    Verifies that the exception is propagated and not caught within the function.
    """
    mock_cursor = Mock()
    mock_cursor.execute.side_effect = Exception("COPY failed")

    with patch('snowflake_ingestion.functions.run_sql_file'):
        # Correction: Patcher le logger dans le module load_to_table directement
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            table_schema = [("vendorid", "NUMBER"), ("tpep_pickup_datetime", "TIMESTAMP_NTZ")]
            with pytest.raises(Exception, match="COPY failed"):
                load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet", table_schema)

def test_update_metadata():
    """Tests the successful update of the metadata table after a file load.
    Verifies the correct UPDATE SQL is executed with the proper parameters
    and that a debug log is recorded.
    """
    mock_cursor = Mock()
    # Correction: Patcher le logger dans le module load_to_table directement
    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
        load.update_metadata(mock_cursor, "test_file.parquet", 250)
        mock_cursor.execute.assert_called_once()
        update_call = mock_cursor.execute.call_args
        assert "UPDATE" in update_call[0][0]
        assert "rows_loaded" in update_call[0][0]
        assert "SUCCESS" in update_call[0][0]
        assert len(update_call[0][1]) == 2
        assert update_call[0][1][0] == 250
        assert update_call[0][1][1] == "test_file.parquet"
        mock_logger.debug.assert_called_with(f"🚀 Loading {load.functions.METADATA_TABLE}")

def test_cleanup_stage_file():
    """Tests the removal of a processed file from the Snowflake stage.
    Verifies the correct REMOVE command is executed and a success log is recorded.
    """
    mock_cursor = Mock()
    # Correction: Patcher le logger dans le module load_to_table directement
    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
        load.cleanup_stage_file(mock_cursor, "test_file.parquet")
        mock_cursor.execute.assert_called_once_with("REMOVE @~/test_file.parquet")
        mock_logger.info.assert_called_with("✅ test_file.parquet removed from stage")

def test_handle_loading_error():
    """Tests the error handling flow when a file fails to load.
    Verifies that an error is logged, the metadata table is updated to 'FAILED_LOAD',
    and a debug log is recorded.
    """
    mock_cursor = Mock()
    test_error = Exception("COPY INTO failed")
    # Correction: Patcher le logger dans le module load_to_table directement
    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
        load.handle_loading_error(mock_cursor, "test_file.parquet", test_error)
        mock_logger.error.assert_called_with(f"❌ Loading error test_file.parquet: COPY INTO failed")
        mock_logger.debug.assert_called_with(f"🚀 Loading {load.functions.METADATA_TABLE}")
        mock_cursor.execute.assert_called_once()
        update_call = mock_cursor.execute.call_args
        assert "FAILED_LOAD" in update_call[0][0]
        assert update_call[0][1] == ("test_file.parquet",)

def test_main_success_flow():
    """Tests the complete successful main execution flow with two files.
    Verifies the full sequence: connection, context setting, table creation,
    fetching staged files, loading each file, updating metadata, and cleanup.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.side_effect = [
        [("file1.parquet",), ("file2.parquet",)],
    ]

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata'):
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                # Correction: Patcher le logger dans le module load_to_table directement
                                with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                    mock_copy.return_value = 100
                                    load.main()
                                    mock_logger.info.assert_any_call("🔍 Analyzing files in STAGE")
                                    assert mock_copy.call_count == 2
                                    mock_copy.assert_any_call(ANY, "file1.parquet", [("vendorid", "NUMBER")])
                                    mock_copy.assert_any_call(ANY, "file2.parquet", [("vendorid", "NUMBER")])

def test_main_with_loading_error():
    """Tests the main flow when one file fails to load.
    Verifies that the error handler is called for the failed file,
    while successful files continue processing normally.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",), ("file2.parquet",)]

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata'):
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                with patch('snowflake_ingestion.load_to_table.handle_loading_error') as mock_handle_error:
                                    # Correction: Patcher le logger dans le module load_to_table directement
                                    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                        def mock_copy_side_effect(cur, filename, table_schema):
                                            if filename == "file1.parquet":
                                                return 100
                                            else:
                                                raise Exception("COPY INTO failed")
                                        mock_copy.side_effect = mock_copy_side_effect
                                        load.main()
                                        assert mock_copy.call_count == 2
                                        mock_handle_error.assert_called_once_with(ANY, "file2.parquet", ANY)

def test_main_no_staged_files():
    """Tests the main flow when no files are found in the stage.
    Verifies that the stage analysis log occurs but no copy operations are attempted.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    # Correction: Patcher le logger dans le module load_to_table directement
                    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                        load.main()
                        mock_logger.info.assert_any_call("🔍 Analyzing files in STAGE")
                        assert not any("COPY INTO" in str(call) for call in mock_cursor.execute.call_args_list)

def test_main_table_creation_error():
    """Tests the main flow when table creation fails.
    Verifies that the exception from create_table propagates and stops the main process.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table') as mock_create_table:
                mock_create_table.side_effect = Exception("Table creation failed")
                with pytest.raises(Exception, match="Table creation failed"):
                    load.main()

def test_main_connection_error():
    """Tests the main flow when the initial database connection fails.
    Verifies that the connection exception propagates and stops the process.
    """
    with patch('snowflake_ingestion.functions.connect_with_role') as mock_connect:
        mock_connect.side_effect = Exception("Connection failed")
        with pytest.raises(Exception, match="Connection failed"):
            load.main()

def test_main_complete_flow_with_counts():
    """Tests a complete successful flow with a single file, verifying precise function call sequence.
    Ensures update_metadata and cleanup_stage_file are called exactly once with the correct arguments.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",)]

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count', return_value=150):
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file') as mock_cleanup:
                                # Correction: Patcher le logger dans le module load_to_table directement
                                with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                    load.main()
                                    mock_update.assert_called_once_with(ANY, "file1.parquet", 150)
                                    mock_cleanup.assert_called_once_with(ANY, "file1.parquet")

def test_main_multiple_files_different_results():
    """Tests processing multiple files with different row counts.
    Verifies that update_metadata is called for each file with its respective row count.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("small_file.parquet",), ("large_file.parquet",)]

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                # Correction: Patcher le logger dans le module load_to_table directement
                                with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                    mock_copy.side_effect = [50, 1000]
                                    load.main()
                                    update_calls = mock_update.call_args_list
                                    assert len(update_calls) == 2
                                    assert update_calls[0][0] == (ANY, "small_file.parquet", 50)
                                    assert update_calls[1][0] == (ANY, "large_file.parquet", 1000)

def test_main_exception_handling_in_loop():
    """Tests error handling within the file processing loop.
    Verifies that an error on one file triggers handle_loading_error for that file,
    while other files continue processing normally (update and cleanup are called for successful files).
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",), ("file2.parquet",), ("file3.parquet",)]

    with patch('snowflake_ingestion.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table', return_value=[("vendorid", "NUMBER")]):
                with patch('snowflake_ingestion.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file') as mock_cleanup:
                                with patch('snowflake_ingestion.load_to_table.handle_loading_error') as mock_handle_error:
                                    # Correction: Patcher le logger dans le module load_to_table directement
                                    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                        def mock_copy_side_effect(cur, filename, table_schema):
                                            if filename == "file2.parquet":
                                                raise Exception("Error on file2")
                                            return 100
                                        mock_copy.side_effect = mock_copy_side_effect
                                        load.main()
                                        assert mock_copy.call_count == 3
                                        mock_handle_error.assert_called_once_with(ANY, "file2.parquet", ANY)
                                        assert mock_update.call_count == 2
                                        assert mock_cleanup.call_count == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])