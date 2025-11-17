import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open, call
import sys
import os
import requests
import shutil

# Ajouter le chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from snowflake_ingestion.upload_stage import (
    download_and_upload_file, main
)
from snowflake_ingestion.upload_stage import SQL_DIR, USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER
from snowflake_ingestion.upload_stage import WH_NAME, DW_NAME, RAW_SCHEMA, METADATA_TABLE


def test_download_and_upload_file_success():
    """Test unitaire de download_and_upload_file en cas de succès.
    
    Vérifie que la fonction télécharge le fichier depuis l'URL, le sauvegarde
    localement, l'upload vers Snowflake via PUT et retourne le chemin temporaire.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.content = b"fake parquet content"
    mock_response.raise_for_status = Mock()
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.open', mock_open()) as mock_file:
            with patch('snowflake_ingestion.upload_stage.os.makedirs'):
                with patch('snowflake_ingestion.upload_stage.os.path.abspath', return_value='/absolute/temp_files/test.parquet'):
                    with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                        
                        result = download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")
                        
                        # Vérifications
                        mock_response.raise_for_status.assert_called_once()
                        mock_file().write.assert_called_once_with(b"fake parquet content")
                        mock_cursor.execute.assert_called_once_with("PUT 'file:///absolute/temp_files/test.parquet' @~ AUTO_COMPRESS=FALSE")
                        mock_logger.info.assert_any_call("📥 Téléchargement de test.parquet...")
                        mock_logger.info.assert_any_call("📤 Upload vers Snowflake...")
                        assert result == "temp_files/test.parquet"


def test_download_and_upload_file_http_error():
    """Test unitaire de download_and_upload_file en cas d'erreur HTTP.
    
    Vérifie que la fonction lève une exception quand le téléchargement HTTP échoue.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.os.makedirs'):
            with pytest.raises(requests.HTTPError):
                download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")


def test_download_and_upload_file_io_error():
    """Test unitaire de download_and_upload_file en cas d'erreur d'écriture.
    
    Vérifie que la fonction lève une exception quand l'écriture du fichier échoue.
    """
    mock_cursor = Mock()
    mock_response = Mock()
    mock_response.content = b"fake parquet content"
    mock_response.raise_for_status = Mock()
    
    with patch('snowflake_ingestion.upload_stage.requests.get', return_value=mock_response):
        with patch('snowflake_ingestion.upload_stage.open', side_effect=IOError("Disk full")):
            with patch('snowflake_ingestion.upload_stage.os.makedirs'):
                with pytest.raises(IOError):
                    download_and_upload_file(mock_cursor, "http://example.com/test.parquet", "test.parquet")


def test_main_with_files():
    """Test unitaire de main avec des fichiers à uploader.
    
    Vérifie que la fonction récupère les fichiers scraped, les télécharge,
    les upload vers Snowflake et met à jour le statut dans les métadonnées.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Mock des fichiers scraped
    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet"),
        ("http://example.com/file2.parquet", "file2.parquet")
    ]
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:
                    with patch('snowflake_ingestion.upload_stage.os.path.exists', return_value=True):
                        with patch('snowflake_ingestion.upload_stage.os.unlink'):
                            with patch('snowflake_ingestion.upload_stage.shutil.rmtree'):
                                with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                                    
                                    mock_download.return_value = "temp_files/file.parquet"
                                    
                                    main()
                                    
                                    # Vérifications
                                    mock_logger.info.assert_any_call("📦 2 fichiers à uploader")
                                    mock_logger.info.assert_any_call("✅ file1.parquet uploadé")
                                    mock_logger.info.assert_any_call("✅ file2.parquet uploadé")
                                    
                                    # Vérifie que les statuts sont mis à jour
                                    update_calls = [call for call in mock_cursor.execute.call_args_list 
                                                  if 'UPDATE' in str(call[0][0]) and 'STAGED' in str(call[0][0])]
                                    assert len(update_calls) == 2


def test_main_without_files():
    """Test unitaire de main sans fichiers à uploader.
    
    Vérifie que la fonction logge un avertissement quand aucun fichier scraped
    n'est disponible pour l'upload.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Aucun fichier scraped
    mock_cursor.fetchall.return_value = []
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                    
                    main()
                    
                    # Vérifie l'avertissement
                    mock_logger.warning.assert_called_with("⚠️  Aucun fichier à uploader")


def test_main_with_upload_error():
    """Test unitaire de main avec erreur d'upload.
    
    Vérifie que la fonction gère correctement les erreurs d'upload en mettant
    à jour le statut FAILED_STAGE et en nettoyant les fichiers temporaires.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet")
    ]
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file') as mock_download:
                    with patch('snowflake_ingestion.upload_stage.os.path.exists', return_value=False):
                        with patch('snowflake_ingestion.upload_stage.shutil.rmtree'):
                            with patch('snowflake_ingestion.upload_stage.logger') as mock_logger:
                                
                                # Simule une erreur d'upload
                                mock_download.side_effect = Exception("Upload failed")
                                
                                main()
                                
                                # Vérifie la gestion d'erreur
                                mock_logger.error.assert_called_with("❌ Erreur upload file1.parquet: Upload failed")
                                
                                # Vérifie que le statut FAILED_STAGE est mis à jour
                                update_calls = [call for call in mock_cursor.execute.call_args_list 
                                              if 'FAILED_STAGE' in str(call[0][0])]
                                assert len(update_calls) == 1


def test_main_cleanup_temp_files():
    """Test unitaire du nettoyage des fichiers temporaires.
    
    Vérifie que la fonction supprime les fichiers temporaires après l'upload
    et nettoie le répertoire temporaire à la fin du processus.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet")
    ]
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file', return_value="temp_files/file1.parquet"):
                    with patch('snowflake_ingestion.upload_stage.os.path.exists', return_value=True):
                        with patch('snowflake_ingestion.upload_stage.os.unlink') as mock_unlink:
                            with patch('snowflake_ingestion.upload_stage.shutil.rmtree') as mock_rmtree:
                                with patch('snowflake_ingestion.upload_stage.logger'):
                                    
                                    main()
                                    
                                    # Vérifie le nettoyage
                                    mock_unlink.assert_called_once_with("temp_files/file1.parquet")
                                    mock_rmtree.assert_called_once_with("temp_files", ignore_errors=True)


def test_main_file_processing_flow():
    """Test unitaire du flux complet de traitement des fichiers.
    
    Vérifie l'ordre des opérations : connexion DB, récupération métadonnées,
    téléchargement, upload, mise à jour statut, et nettoyage.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    mock_cursor.fetchall.return_value = [
        ("http://example.com/test.parquet", "test.parquet")
    ]
    
    # Liste pour suivre les appels à execute
    execute_calls = []
    
    def track_execute(*args, **kwargs):
        execute_calls.append((args, kwargs))
        return MagicMock()
    
    mock_cursor.execute.side_effect = track_execute
    
    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file', return_value="temp_files/test.parquet"):
                    with patch('snowflake_ingestion.upload_stage.os.path.exists', return_value=True):
                        with patch('snowflake_ingestion.upload_stage.os.unlink'):
                            with patch('snowflake_ingestion.upload_stage.shutil.rmtree'):
                                with patch('snowflake_ingestion.upload_stage.logger'):
                                    
                                    main()
                                    
                                    # Vérifie que l'UPDATE STAGED est bien appelé avec le bon paramètre
                                    staged_updates = []
                                    for args, kwargs in execute_calls:
                                        if len(args) > 0 and 'UPDATE' in args[0] and 'STAGED' in args[0]:
                                            staged_updates.append((args, kwargs))
                                    
                                    assert len(staged_updates) == 1
                                    # Vérifie que le paramètre est le bon nom de fichier
                                    update_args, update_kwargs = staged_updates[0]
                                    assert len(update_args) >= 2
                                    assert update_args[1] == ('test.parquet',)


def test_main_tmp_path_none_handling():
    """Test unitaire de la gestion de tmp_path=None dans le bloc finally.

    Vérifie que la fonction gère correctement le cas où tmp_path est None
    et évite l'erreur UnboundLocalError.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ("http://example.com/file1.parquet", "file1.parquet")
    ]

    with patch('snowflake_ingestion.upload_stage.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.upload_stage.use_context'):
            with patch('snowflake_ingestion.upload_stage.run_sql_file'):
                with patch('snowflake_ingestion.upload_stage.download_and_upload_file', side_effect=Exception("Test error")):
                    with patch('snowflake_ingestion.upload_stage.os.path.exists') as mock_exists:
                        with patch('snowflake_ingestion.upload_stage.os.unlink') as mock_unlink:
                            with patch('snowflake_ingestion.upload_stage.shutil.rmtree'):
                                with patch('snowflake_ingestion.upload_stage.logger'):

                                    # Ce test vérifie qu'aucune exception n'est levée
                                    try:
                                        main()
                                        # Si nous arrivons ici, c'est que l'erreur a été évitée
                                        assert True
                                    except Exception as e:
                                        assert False, f"Exception non gérée correctement: {e}"

                                    # Vérifie que os.path.exists n'est pas appelé car tmp_path est None
                                    mock_exists.assert_not_called()
                                    # Vérifie que os.unlink n'est pas appelé non plus
                                    mock_unlink.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])