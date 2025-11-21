import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open, call
import sys
import os
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from snowflake_ingestion.upload_stage import *

def test_download_and_upload_file_success():
    """Test unitaire de download_and_upload_file en cas de succès.
    Vérifie que la fonction télécharge le fichier depuis l'URL, l'upload vers Snowflake
    via PUT, et nettoie automatiquement le fichier temporaire.
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
                download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")
                
                mock_response.raise_for_status.assert_called_once()
                mock_temp_file.write.assert_called_once_with(b"fake parquet content")
                mock_temp_file.flush.assert_called_once()
                mock_cursor.execute.assert_called_once_with("PUT 'file:///tmp/tempfile_123.parquet' @~/test.parquet AUTO_COMPRESS=FALSE")
                mock_logger.info.assert_any_call("📥 Téléchargement de test.parquet...")
                mock_logger.info.assert_any_call("📤 Upload vers Snowflake...")
                mock_logger.info.assert_any_call("✅ test.parquet uploadé et fichier temporaire nettoyé")


def test_download_and_upload_file_http_error():
    """Test unitaire de download_and_upload_file en cas d'erreur HTTP.
    Vérifie que la fonction lève une exception quand le téléchargement HTTP échoue.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.tempfile.NamedTemporaryFile'):
            with patch('snowflake_ingestion.upload_stage.logger'):
                with pytest.raises(requests.HTTPError):
                    download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")


def test_download_and_upload_file_snowflake_error():
    """Test unitaire de download_and_upload_file en cas d'erreur Snowflake.
    Vérifie que la fonction lève une exception quand l'upload vers Snowflake échoue.
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
                    download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")


def test_download_and_upload_file_tempfile_error():
    """Test unitaire de download_and_upload_file en cas d'erreur de création du fichier temporaire.
    Vérifie que la fonction lève une exception quand la création du fichier temporaire échoue.
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
                    download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")



def test_main_with_files():
    """Test unitaire de main avec des fichiers à uploader.
    Vérifie que la fonction récupère les fichiers scraped, les télécharge,
    les upload vers Snowflake et met à jour le statut dans les métadonnées.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet"),
        ("http://example.com/file2.parquet", "file2.parquet")
    ]
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:  
                    with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:   
                        main()
                        mock_logger.info.assert_any_call("📦 2 fichiers à uploader")
                        mock_logger.info.assert_any_call("✅ file1.parquet uploadé")
                        mock_logger.info.assert_any_call("✅ file2.parquet uploadé")
                        update_calls = [call for call in mock_cursor.execute.call_args_list 
                                      if 'UPDATE' in str(call[0][0]) and 'STAGED' in str(call[0][0])]
                        assert len(update_calls) == 2


def test_main_with_upload_error():
    """Test unitaire de main avec erreur d'upload.
    Vérifie que la fonction gère correctement les erreurs d'upload en mettant
    à jour le statut FAILED_STAGE.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [("http://example.com/file1.parquet", "file1.parquet")]
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:
                    with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                        mock_download.side_effect = Exception("Upload failed")
                        main()

                        mock_logger.error.assert_called_with("❌ Erreur upload file1.parquet: Upload failed")
                        update_calls = [call for call in mock_cursor.execute.call_args_list 
                                      if 'FAILED_STAGE' in str(call[0][0])]
                        assert len(update_calls) == 1



def test_main_file_processing_flow():
    """Test unitaire du flux complet de traitement des fichiers.
    Vérifie l'ordre des opérations : connexion DB, récupération métadonnées,
    téléchargement, upload, mise à jour statut.
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
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file'):
                    with patch('snowflake_ingestion.upload_stage.logger'):
                        
                        main()

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