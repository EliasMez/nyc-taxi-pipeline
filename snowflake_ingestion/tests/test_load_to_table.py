import pytest
from unittest.mock import Mock, patch, MagicMock, ANY
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.load_to_table as load


def test_create_table_success():
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        ("vendor_id", "NUMBER"),
        ("tpep_pickup_datetime", "TIMESTAMP_NTZ"),
        ("tpep_dropoff_datetime", "TIMESTAMP_NTZ")
    ]
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            load.create_table(mock_cursor)

            mock_run_sql.assert_any_call(mock_cursor, load.SQL_DIR / "detect_file_schema_stage.sql")
            mock_run_sql.assert_any_call(mock_cursor, load.SQL_DIR / "add_filename_to_raw_table.sql")
            mock_cursor.execute.assert_called_once()
            create_call = mock_cursor.execute.call_args[0][0]
            assert "CREATE TABLE IF NOT EXISTS" in create_call
            assert "vendor_id NUMBER" in create_call
            assert "tpep_pickup_datetime TIMESTAMP_NTZ" in create_call
            # CORRECTION : Utilisation de functions.RAW_TABLE
            mock_logger.info.assert_any_call(f"📋 Vérification/Création dynamique de la table {load.functions.RAW_TABLE}")
            mock_logger.info.assert_any_call(f"✅ Table {load.functions.RAW_TABLE} prête")


def test_create_table_no_schema():
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = []
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            load.create_table(mock_cursor)
            mock_logger.warning.assert_called_with("⚠️  Aucune donnée dans le STAGE")
            mock_cursor.execute.assert_not_called()


def test_copy_file_to_table_and_count_success():
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('test_file.parquet', 'LOADED', 250, 250, 1, 0, None, None, None, None)
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            result = load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet")
            assert result == 250
            mock_cursor.execute.assert_any_call(ANY, ('test_file.parquet',))


def test_copy_file_to_table_and_count_zero_loaded():
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('Copy executed with 0 files processed.',)
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
        with patch('snowflake_ingestion.load_to_table.logger'):
            result = load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet")
            assert result == 0


def test_copy_file_to_table_and_count_update_error():
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('test_file.parquet', 'LOADED', 100, 100, 1, 0, None, None, None, None)
    mock_cursor.execute.side_effect = [None, Exception("Update failed")]
    
    with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
        with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
            with pytest.raises(Exception):
                load.copy_file_to_table_and_count(mock_cursor, "test_file.parquet")


def test_update_metadata():
    mock_cursor = Mock()
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
        # CORRECTION : Utilisation de functions.METADATA_TABLE
        mock_logger.debug.assert_called_with(f"🚀 Chargement de {load.functions.METADATA_TABLE}")


def test_cleanup_stage_file():
    mock_cursor = Mock()
    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
        load.cleanup_stage_file(mock_cursor, "test_file.parquet")
        mock_cursor.execute.assert_called_once_with("REMOVE @~/test_file.parquet")
        mock_logger.info.assert_called_with("✅ test_file.parquet supprimé du stage")


def test_handle_loading_error():
    mock_cursor = Mock()
    test_error = Exception("COPY INTO failed")
    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
        load.handle_loading_error(mock_cursor, "test_file.parquet", test_error)
        mock_logger.error.assert_called_with("❌ Erreur de chargement test_file.parquet: COPY INTO failed")
        # CORRECTION : Utilisation de functions.METADATA_TABLE
        mock_logger.debug.assert_called_with(f"🚀 Chargement de {load.functions.METADATA_TABLE}")
        mock_cursor.execute.assert_called_once()
        update_call = mock_cursor.execute.call_args
        assert "FAILED_LOAD" in update_call[0][0]
        assert update_call[0][1] == ("test_file.parquet",)


def test_main_success_flow():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",), ("file2.parquet",)]

    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata'):
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                                    mock_copy.return_value = 100         
                                    load.main()
                                    mock_logger.info.assert_any_call("🔍 Analyse des fichiers dans le STAGE")
                                    assert mock_copy.call_count == 2
                                    mock_copy.assert_any_call(ANY, "file1.parquet")
                                    mock_copy.assert_any_call(ANY, "file2.parquet")


def test_main_with_loading_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",), ("file2.parquet",)]
    
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata'):
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                with patch('snowflake_ingestion.load_to_table.handle_loading_error') as mock_handle_error:
                                    with patch('snowflake_ingestion.load_to_table.logger'):
                                        def mock_copy_side_effect(cur, filename):
                                            if filename == "file1.parquet":
                                                return 100
                                            else:
                                                raise Exception("COPY INTO failed")
                                        mock_copy.side_effect = mock_copy_side_effect
                                        load.main()
                                        assert mock_copy.call_count == 2
                                        mock_handle_error.assert_called_once_with(ANY, "file2.parquet", ANY)


def test_main_no_staged_files():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.logger') as mock_logger:
                        load.main()
                        mock_logger.info.assert_any_call("🔍 Analyse des fichiers dans le STAGE")
                        assert not any("COPY INTO" in str(call) for call in mock_cursor.execute.call_args_list)


def test_main_table_creation_error():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table') as mock_create_table:
                mock_create_table.side_effect = Exception("Table creation failed")
                with pytest.raises(Exception, match="Table creation failed"):
                    load.main()


def test_main_connection_error():
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role') as mock_connect:
        mock_connect.side_effect = Exception("Connection failed")
        with pytest.raises(Exception, match="Connection failed"):
            load.main()


def test_main_complete_flow_with_counts():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",)]
    
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count', return_value=150):
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file') as mock_cleanup:
                                with patch('snowflake_ingestion.load_to_table.logger'):
                                    load.main()
                                    mock_update.assert_called_once_with(ANY, "file1.parquet", 150)
                                    mock_cleanup.assert_called_once_with(ANY, "file1.parquet")


def test_main_multiple_files_different_results():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("small_file.parquet",),("large_file.parquet",)]
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file'):
                                with patch('snowflake_ingestion.load_to_table.logger'):
                                    mock_copy.side_effect = [50, 1000]
                                    load.main()
                                    update_calls = mock_update.call_args_list
                                    assert len(update_calls) == 2
                                    assert update_calls[0][0] == (ANY, "small_file.parquet", 50)
                                    assert update_calls[1][0] == (ANY, "large_file.parquet", 1000)


def test_main_exception_handling_in_loop():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("file1.parquet",),("file2.parquet",),("file3.parquet",)]
    
    with patch('snowflake_ingestion.load_to_table.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.load_to_table.functions.use_context'):
            with patch('snowflake_ingestion.load_to_table.create_table'):
                with patch('snowflake_ingestion.load_to_table.functions.run_sql_file'):
                    with patch('snowflake_ingestion.load_to_table.copy_file_to_table_and_count') as mock_copy:
                        with patch('snowflake_ingestion.load_to_table.update_metadata') as mock_update:
                            with patch('snowflake_ingestion.load_to_table.cleanup_stage_file') as mock_cleanup:
                                with patch('snowflake_ingestion.load_to_table.handle_loading_error') as mock_handle_error:
                                    with patch('snowflake_ingestion.load_to_table.logger'):
                                        def mock_copy_side_effect(cur, filename):
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