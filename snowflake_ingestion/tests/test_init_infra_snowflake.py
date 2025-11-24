from unittest.mock import Mock, patch
import snowflake_ingestion.init_infra_snowflake as infra

def test_setup_data_warehouse():
    """Test unitaire de la fonction setup_data_warehouse.
    Vérifie que la fonction appelle functions.run_sql_file avec le bon fichier SQL
    et logge les messages appropriés pour la création du warehouse et des schémas.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.setup_data_warehouse(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "setup_data_warehouse.sql")
            mock_logger.info.assert_any_call("🏗️  Création du warehouse, base et schémas...")
            mock_logger.info.assert_any_call("✅ Warehouse et schémas créés")


def test_create_roles_and_user():
    """Test unitaire de la fonction create_roles_and_user.
    Vérifie que la fonction appelle functions.run_sql_file avec le bon fichier SQL
    et logge les messages appropriés pour la création des rôles et utilisateurs.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.create_roles_and_user(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "create_roles_and_user.sql")
            mock_logger.info.assert_any_call("🔐 Création du rôle et de l'utilisateur DBT...")
            mock_logger.info.assert_any_call("✅ Rôle et utilisateur créés")


def test_grant_privileges():
    """Test unitaire de la fonction grant_privileges.
    Vérifie que la fonction appelle functions.run_sql_file avec le bon fichier SQL
    et logge les messages appropriés pour l'attribution des privilèges.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.grant_privileges(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "grant_privileges.sql")
            mock_logger.info.assert_any_call("🔑 Attribution des privilèges au rôle TRANSFORMER...")
            mock_logger.info.assert_any_call("✅ Privilèges attribués")


def test_main_success():
    """Test unitaire de la fonction main en cas de succès.
    Vérifie que la fonction établit les connexions avec les bons rôles,
    exécute les étapes dans l'ordre et logge le message de succès final.
    """
    mock_conn = Mock()
    mock_cursor = Mock()

    mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = Mock(return_value=None)
    
    with patch('snowflake_ingestion.init_infra_snowflake.functions.connect_with_role', return_value=mock_conn) as mock_connect:
        with patch('snowflake_ingestion.init_infra_snowflake.setup_data_warehouse') as mock_setup:
            with patch('snowflake_ingestion.init_infra_snowflake.create_roles_and_user') as mock_create:
                with patch('snowflake_ingestion.init_infra_snowflake.grant_privileges') as mock_grant:
                    with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
                        infra.main()

                        assert mock_connect.call_count == 2
                        mock_connect.assert_any_call(infra.functions.USER, infra.functions.PASSWORD, infra.functions.ACCOUNT, 'SYSADMIN')
                        mock_connect.assert_any_call(infra.functions.USER, infra.functions.PASSWORD, infra.functions.ACCOUNT, 'SECURITYADMIN')
                        
                        mock_setup.assert_called_once()
                        mock_create.assert_called_once()
                        mock_grant.assert_called_once()
                        mock_logger.info.assert_called_with("🎯 Initialisation complète terminée avec succès !")


def test_main_exception():
    """Test unitaire de la fonction main en cas d'erreur.
    Vérifie que la fonction logge l'erreur et ne lève pas d'exception
    lorsqu'une erreur se produit pendant l'initialisation.
    """
    with patch('snowflake_ingestion.init_infra_snowflake.functions.connect_with_role', side_effect=Exception("Connection failed")):
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.main()
            mock_logger.error.assert_called_once()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])