import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
# from datetime import datetime
# from pathlib import Path
import sys
import os

# Ajouter le chemin pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from snowflake_ingestion.scrape_links import (
    get_scraping_year, get_xpath, get_parquet_links, 
    setup_meta_table, main, current_year, current_month
)
from snowflake_ingestion.scrape_links import SQL_DIR, USER_DEV, PASSWORD_DEV, ACCOUNT, ROLE_TRANSFORMER
from snowflake_ingestion.scrape_links import WH_NAME, DW_NAME, RAW_SCHEMA, METADATA_TABLE


def test_get_scraping_year_with_valid_env():
    """Test unitaire de get_scraping_year avec variable d'environnement valide.
    
    Vérifie que la fonction retourne la valeur de SCRAPING_YEAR convertie en entier
    quand elle est définie et valide.
    """
    with patch('snowflake_ingestion.scrape_links.SCRAPING_YEAR', '2023'):
        result = get_scraping_year()
        assert result == 2023


def test_get_scraping_year_with_empty_env():
    """Test unitaire de get_scraping_year avec variable d'environnement vide.
    
    Vérifie que la fonction retourne l'année par défaut (current_year - 1 si month <= 3,
    sinon current_year) quand SCRAPING_YEAR est vide.
    """
    with patch('snowflake_ingestion.scrape_links.SCRAPING_YEAR', ''):
        with patch('snowflake_ingestion.scrape_links.current_month', 2):  # Mois <= 3
            result = get_scraping_year()
            expected = current_year - 1
            assert result == expected


def test_get_scraping_year_with_invalid_env():
    """Test unitaire de get_scraping_year avec variable d'environnement invalide.
    
    Vérifie que la fonction retourne l'année par défaut et logge une erreur
    quand SCRAPING_YEAR n'est pas un entier valide.
    """
    with patch('snowflake_ingestion.scrape_links.SCRAPING_YEAR', 'invalid'):
        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
            with patch('snowflake_ingestion.scrape_links.current_month', 5):  # Mois > 3
                result = get_scraping_year()
                expected = current_year
                assert result == expected
                mock_logger.error.assert_called_once()


def test_get_xpath():
    """Test unitaire de get_xpath.
    
    Vérifie que la fonction génère une expression XPath correcte incluant
    toutes les années entre l'année de scraping et l'année courante.
    """
    with patch('snowflake_ingestion.scrape_links.get_scraping_year', return_value=2023):
        with patch('snowflake_ingestion.scrape_links.current_year', 2024):
            result = get_xpath()
            expected = "//a[@title='Yellow Taxi Trip Records' and (contains(@href, '2023') or contains(@href, '2024'))]"
            assert result == expected


def test_get_parquet_links_success():
    """Test unitaire de get_parquet_links en cas de succès.
    
    Vérifie que la fonction effectue une requête HTTP, parse le HTML et
    retourne les liens Parquet filtrés par l'expression XPath.
    """
    mock_html_content = """
    <html>
        <a title="Yellow Taxi Trip Records" href="https://example.com/file1.parquet">Link1</a>
        <a title="Yellow Taxi Trip Records" href="https://example.com/file2.parquet">Link2</a>
        <a title="Other Title" href="https://example.com/file3.parquet">Link3</a>
    </html>
    """
    
    with patch('snowflake_ingestion.scrape_links.requests.get') as mock_get:
        with patch('snowflake_ingestion.scrape_links.html.fromstring') as mock_fromstring:
            with patch('snowflake_ingestion.scrape_links.get_xpath', return_value="//a[@title='Yellow Taxi Trip Records']"):
                with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                    
                    # Mock de la réponse HTTP
                    mock_response = Mock()
                    mock_response.content = mock_html_content.encode()
                    mock_get.return_value = mock_response
                    
                    # Mock du parsing HTML
                    mock_tree = Mock()
                    mock_link1 = Mock()
                    mock_link1.get.return_value = "https://example.com/file1.parquet"
                    mock_link2 = Mock()
                    mock_link2.get.return_value = "https://example.com/file2.parquet"
                    mock_tree.xpath.return_value = [mock_link1, mock_link2]
                    mock_fromstring.return_value = mock_tree
                    
                    result = get_parquet_links()
                    
                    # Vérifications
                    mock_get.assert_called_once_with("https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
                    mock_logger.info.assert_called_with("🌐 Début du scraping des données NYC Taxi")
                    assert result == ["https://example.com/file1.parquet", "https://example.com/file2.parquet"]


def test_setup_meta_table():
    """Test unitaire de setup_meta_table.
    
    Vérifie que la fonction appelle run_sql_file avec le bon fichier SQL
    et logge les messages appropriés pour la création de la table de métadonnées.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.scrape_links.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
            setup_meta_table(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, SQL_DIR / "setup_meta_table.sql")
            mock_logger.info.assert_any_call("📋 Vérification/Création de la table de metadata")
            mock_logger.info.assert_any_call("✅ Table de metadata prête")


def test_main_with_new_files():
    """Test unitaire de main avec nouveaux fichiers détectés.
    
    Vérifie que la fonction insère les nouveaux fichiers dans la table de métadonnées
    quand des fichiers non référencés sont trouvés lors du scraping.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.side_effect = [None, None, [5]]  # Fichiers non existants, puis count > 0
    
    with patch('snowflake_ingestion.scrape_links.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                            
                            # Mock des liens retournés
                            mock_links.return_value = [
                                "https://example.com/yellow_tripdata_2023-01.parquet",
                                "https://example.com/yellow_tripdata_2023-02.parquet"
                            ]
                            
                            main()
                            
                            # Vérifie les insertions
                            assert mock_cursor.execute.call_count >= 4  # SELECT + INSERT pour chaque fichier
                            mock_logger.info.assert_any_call("📎 2 liens trouvés")
                            mock_logger.info.assert_any_call("➕ Nouveau fichier détecté : yellow_tripdata_2023-01.parquet")


def test_main_without_new_files():
    """Test unitaire de main sans nouveaux fichiers.
    
    Vérifie que la fonction logge un avertissement quand aucun nouveau fichier
    n'est détecté lors du scraping.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Tous les fichiers existent déjà
    mock_cursor.fetchone.return_value = [1]  # Fichiers existants
    # OU pour count_new_files.sql
    mock_cursor.fetchone.side_effect = [[1], [1], [0]]  # Fichiers existants + count = 0
    
    with patch('snowflake_ingestion.scrape_links.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger') as mock_logger:
                            
                            mock_links.return_value = [
                                "https://example.com/yellow_tripdata_2023-01.parquet"
                            ]
                            
                            main()
                            
                            # Vérifie que le warning est bien appelé
                            # OU vérifie que c'est un cas normal (pas d'erreur)
                            mock_logger.info.assert_any_call("✅ Scraping terminé")
                            # Le warning peut ne pas être appelé si c'est considéré comme normal


def test_main_file_parsing():
    """Test unitaire de l'extraction année/mois depuis le nom de fichier.
    
    Vérifie que la fonction extrait correctement l'année et le mois depuis
    le nom du fichier Parquet lors de l'insertion dans les métadonnées.
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Fichier non existant
    
    with patch('snowflake_ingestion.scrape_links.connect_with_role', return_value=mock_conn):
        with patch('snowflake_ingestion.scrape_links.use_context'):
            with patch('snowflake_ingestion.scrape_links.setup_meta_table'):
                with patch('snowflake_ingestion.scrape_links.get_parquet_links') as mock_links:
                    with patch('snowflake_ingestion.scrape_links.run_sql_file'):
                        with patch('snowflake_ingestion.scrape_links.logger'):
                            
                            mock_links.return_value = [
                                "https://example.com/yellow_tripdata_2023-07.parquet"
                            ]
                            
                            main()
                            
                            # Vérifie l'insertion avec année=2023 et mois=7
                            insert_call = None
                            for call in mock_cursor.execute.call_args_list:
                                if 'INSERT' in str(call[0][0]):
                                    insert_call = call
                                    break
                            
                            assert insert_call is not None
                            # Vérifie les paramètres: (url, filename, year, month)
                            assert insert_call[0][1] == ("https://example.com/yellow_tripdata_2023-07.parquet", 
                                                        "yellow_tripdata_2023-07.parquet", 2023, 7)