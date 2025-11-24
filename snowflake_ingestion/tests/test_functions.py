import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from snowflake_ingestion.functions import connect_with_role, use_context, run_sql_file

def test_connect_with_role_success():
    """Test unitaire de connect_with_role en cas de succès.
    Vérifie que la fonction appelle snowflake.connector.connect avec les bons
    paramètres, active l'autocommit et retourne l'objet connexion.
    """
    mock_connection = Mock()
    with patch('snowflake_ingestion.functions.snowflake.connector.connect', return_value=mock_connection) as mock_connect:
        result = connect_with_role("user", "pass", "account", "role")
        mock_connect.assert_called_once_with(
            user="user",
            password="pass", 
            account="account",
            role="role",
            autocommit=True
        )
        assert result == mock_connection


def test_connect_with_role_autocommit_enabled():
    """Test unitaire vérifiant que l'autocommit est toujours activé.
    Vérifie que le paramètre autocommit=True est systématiquement passé
    à la connexion Snowflake, indépendamment des autres paramètres.
    """
    mock_connection = Mock()
    with patch('snowflake_ingestion.functions.snowflake.connector.connect', return_value=mock_connection) as mock_connect:
        connect_with_role("different_user", "different_pass", "different_account", "different_role")
        call_kwargs = mock_connect.call_args.kwargs
        assert call_kwargs['autocommit'] == True


def test_connect_with_role_parameters_passed_correctly():
    """Test unitaire vérifiant la transmission correcte des paramètres.
    Vérifie que tous les paramètres (user, password, account, role) sont
    correctement transmis à snowflake.connector.connect sans modification.
    """
    mock_connection = Mock()
    with patch('snowflake_ingestion.functions.snowflake.connector.connect', return_value=mock_connection) as mock_connect:
        test_params = {
            'user': 'test_user',
            'password': 'test_password', 
            'account': 'test_account',
            'role': 'test_role'
        }
        connect_with_role(**test_params)
        call_kwargs = mock_connect.call_args.kwargs
        for key, value in test_params.items():
            assert call_kwargs[key] == value
        assert call_kwargs['autocommit'] == True




def test_use_context(mocker):
    """Test unitaire de la fonction use_context.
    Vérifie que la fonction exécute les 3 commandes SQL attendues pour configurer
    le contexte Snowflake (warehouse, database, schema) dans le bon ordre.
    
    Args:
        mocker: Fixture pytest pour le mocking
    """
    mock_cursor = Mock()
    with patch.object(mock_cursor, 'execute') as mock_execute:
        use_context(mock_cursor, "WH", "DB", "SCHEMA")
        assert mock_execute.call_count == 3
        calls = [call[0][0] for call in mock_execute.call_args_list]
        assert "USE WAREHOUSE WH" in calls
        assert "USE DATABASE DB" in calls  
        assert "USE SCHEMA SCHEMA" in calls


def test_use_context_exception():
    """Test unitaire de la gestion d'erreur de use_context.
    Vérifie que la fonction lève une exception SystemExit lorsqu'une erreur
    se produit lors de l'exécution des commandes SQL.
    """
    mock_cursor = Mock()
    mock_cursor.execute.side_effect = Exception("DB error")
    
    with pytest.raises(SystemExit):
        use_context(mock_cursor, "WH", "DB", "SCHEMA")




def test_run_sql_file():
    """Test unitaire de la fonction run_sql_file avec substitution de variables.
    Vérifie que les placeholders dans le SQL sont correctement remplacés
    par les valeurs des variables globales correspondantes.
    """
    mock_cursor = Mock()
    sql_content = "SELECT * FROM RAW_TABLE_PLACEHOLDER WHERE user = USER_PLACEHOLDER;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        with patch('snowflake_ingestion.functions.RAW_TABLE', 'my_table'):
            with patch('snowflake_ingestion.functions.USER', 'test_user'):
                run_sql_file(mock_cursor, Path("test.sql"))
    mock_cursor.execute.assert_called_once_with("SELECT * FROM my_table WHERE user = test_user")


def test_run_sql_file_variable_not_found():
    """Test unitaire de run_sql_file avec variable non trouvée.
    Vérifie que les placeholders sans variable globale correspondante
    sont remplacés par la valeur par défaut <VAR_NOT_FOUND>.
    """
    mock_cursor = Mock()
    sql_content = "SELECT * FROM UNKNOWN_PLACEHOLDER;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        run_sql_file(mock_cursor, Path("test.sql"))
    mock_cursor.execute.assert_called_once_with("SELECT * FROM <UNKNOWN_NOT_FOUND>")


def test_run_sql_file_multiple_statements():
    """Test unitaire de run_sql_file avec multiples requêtes.
    Vérifie que les requêtes séparées par des points-virgules sont
    correctement divisées et exécutées individuellement.
    """
    mock_cursor = Mock()
    sql_content = "SELECT 1; SELECT 2; SELECT 3;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        run_sql_file(mock_cursor, Path("test.sql"))
    assert mock_cursor.execute.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])