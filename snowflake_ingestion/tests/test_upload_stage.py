import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import snowflake_ingestion.upload_stage as stage

def test_download_and_upload_file_success():
    """Unit test for download_and_upload_file in case of success.
    Verifies that the function downloads the file from the URL, uploads it to Snowflake
    via PUT, and automatically cleans up the temporary file.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.content = b"fake parquet content"
    mock_response.raise_for_status = Mock()
    mock_temp_file = Mock()
    mock_temp_file.name = "/tmp/tempfile_123.parquet"
    mock_temp_file.write = Mock()
    mock_temp_file.flush = Mock()
    mock_temp_file.__enter__ = Mock(return_value=mock_temp_file)
    mock_temp_file.__exit__ = Mock(return_value=None)
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.tempfile.NamedTemporaryFile') as mock_tempfile:
            with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                mock_tempfile.return_value = mock_temp_file
                stage.download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")
                
                mock_response.raise_for_status.assert_called_once()
                mock_temp_file.write.assert_called_once_with(b"fake parquet content")
                mock_temp_file.flush.assert_called_once()
                mock_cursor.execute.assert_called_once_with("PUT 'file:///tmp/tempfile_123.parquet' @~/test.parquet AUTO_COMPRESS=FALSE")
                mock_logger.info.assert_any_call("📥 Downloading test.parquet...")
                mock_logger.info.assert_any_call("📤 Uploading to Snowflake...")
                mock_logger.info.assert_any_call("✅ test.parquet uploaded and temporary file cleaned")

def test_download_and_upload_file_http_error():
    """Unit test for download_and_upload_file in case of HTTP error.
    Verifies that the function raises an exception when the HTTP download fails.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.tempfile.NamedTemporaryFile'):
            with patch('snowflake_ingestion.upload_stage.logger'):
                with pytest.raises(requests.HTTPError):
                    stage.download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")

def test_download_and_upload_file_snowflake_error():
    """Unit test for download_and_upload_file in case of Snowflake error.
    Verifies that the function raises an exception when the Snowflake upload fails.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.content = b"fake parquet content"
    mock_response.raise_for_status = Mock()
    mock_temp_file = Mock()
    mock_temp_file.name = "/tmp/tempfile_123.parquet"
    mock_temp_file.write = Mock()
    mock_temp_file.flush = Mock()
    mock_temp_file.__enter__ = Mock(return_value=mock_temp_file)
    mock_temp_file.__exit__ = Mock(return_value=None)
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.tempfile.NamedTemporaryFile', return_value=mock_temp_file):
            with patch('snowflake_ingestion.upload_stage.logger'):
                mock_cursor.execute.side_effect = Exception("Snowflake PUT failed")       
                with pytest.raises(Exception, match="Snowflake PUT failed"):
                    stage.download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")

def test_download_and_upload_file_tempfile_error():
    """Unit test for download_and_upload_file in case of temporary file creation error.
    Verifies that the function raises an exception when temporary file creation fails.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.content = b"fake parquet content"
    mock_response.raise_for_status = Mock()
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.tempfile.NamedTemporaryFile') as mock_tempfile:
            with patch('snowflake_ingestion.upload_stage.logger'):
                mock_tempfile.side_effect = OSError("Cannot create temp file")
                with pytest.raises(OSError, match="Cannot create temp file"):
                    stage.download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")

def test_main_with_files():
    """Unit test for the main function with files to upload.
    Verifies that the function retrieves the scraped files, downloads them,
    uploads them to Snowflake and updates the status in the metadata.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet"),
        ("http://example.com/file2.parquet", "file2.parquet")
    ]
    
    with patch('snowflake_ingestion.upload_stage.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.functions.use_context'):
            with patch('snowflake_ingestion.upload_stage.functions.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:
                    with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                        stage.main()
                        mock_logger.info.assert_any_call("📦 2 files to upload")
                        mock_logger.info.assert_any_call("✅ file1.parquet uploaded")
                        mock_logger.info.assert_any_call("✅ file2.parquet uploaded")
                        update_calls = [call for call in mock_cursor.execute.call_args_list 
                                      if 'UPDATE' in str(call[0][0]) and 'STAGED' in str(call[0][0])]
                        assert len(update_calls) == 2

def test_main_with_upload_error():
    """Unit test for the main function with upload error.
    Verifies that the function correctly handles upload errors by updating
    the status to FAILED_STAGE.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("http://example.com/file1.parquet", "file1.parquet")]
    
    with patch('snowflake_ingestion.upload_stage.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.functions.use_context'):
            with patch('snowflake_ingestion.upload_stage.functions.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:
                    with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                        mock_download.side_effect = Exception("Upload failed")
                        stage.main()
                        mock_logger.error.assert_called_with("❌ Upload error file1.parquet: Upload failed")
                        update_calls = [call for call in mock_cursor.execute.call_args_list 
                                      if 'FAILED_STAGE' in str(call[0][0])]
                        assert len(update_calls) == 1

def test_main_file_processing_flow():
    """Unit test for the complete file processing flow.
    Verifies the order of operations: DB connection, metadata retrieval,
    download, upload, status update.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [("http://example.com/test.parquet", "test.parquet")]
    execute_calls = []
    
    def track_execute(*args, **kwargs):
        execute_calls.append((args, kwargs))
        return MagicMock()
    
    mock_cursor.execute.side_effect = track_execute
    
    with patch('snowflake_ingestion.upload_stage.functions.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.functions.use_context'):
            with patch('snowflake_ingestion.upload_stage.functions.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file'):
                    with patch('snowflake_ingestion.upload_stage.logger'):
                        stage.main()
                        staged_updates = []
                        for args, kwargs in execute_calls:
                            if len(args) > 0 and 'UPDATE' in args[0] and 'STAGED' in args[0]:
                                staged_updates.append((args, kwargs))
                        assert len(staged_updates) == 1
                        update_args = staged_updates[0][0]
                        assert len(update_args) >= 2
                        assert update_args[1] == ('test.parquet',)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])