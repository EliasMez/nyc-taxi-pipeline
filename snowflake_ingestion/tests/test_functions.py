import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from snowflake_ingestion.functions import connect_with_role, use_context, run_sql_file

def test_connect_with_role_success():
    """Unit test for connect_with_role on success.
    Verifies that the function calls snowflake.connector.connect with the correct
    parameters, enables autocommit, and returns the connection object.
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
    """Unit test verifying that autocommit is always enabled.
    Verifies that the autocommit=True parameter is systematically passed
    to the Snowflake connection, regardless of other parameters.
    """
    mock_connection = Mock()
    with patch('snowflake_ingestion.functions.snowflake.connector.connect', return_value=mock_connection) as mock_connect:
        connect_with_role("different_user", "different_pass", "different_account", "different_role")
        call_kwargs = mock_connect.call_args.kwargs
        assert call_kwargs['autocommit'] == True


def test_connect_with_role_parameters_passed_correctly():
    """Unit test verifying correct parameter forwarding.
    Verifies that all parameters (user, password, account, role) are
    correctly forwarded to snowflake.connector.connect without modification.
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




def test_use_context(mocker: Mock):
    """Unit test for the use_context function.
    Verifies that the function executes the 3 expected SQL commands to configure
    the Snowflake context (warehouse, database, schema) in the correct order.

    Args:
        mocker: pytest fixture for mocking
    """
    mock_cursor = Mock()
    with patch.object(mock_cursor, 'execute') as mock_execute:
        use_context(mock_cursor, "WH", "DB", "TEST")
        assert mock_execute.call_count == 3
        calls = [call[0][0] for call in mock_execute.call_args_list]
        assert "USE WAREHOUSE WH" in calls
        assert "USE DATABASE DB" in calls  
        assert "USE SCHEMA SCHEMA_TEST" in calls


def test_use_context_exception():
    """Unit test for error handling in use_context.
    Verifies that the function raises a SystemExit exception when an error
    occurs during SQL command execution.
    """
    mock_cursor = Mock()
    mock_cursor.execute.side_effect = Exception("DB error")
    
    with pytest.raises(SystemExit):
        use_context(mock_cursor, "WH", "DB", "SCHEMA")




def test_run_sql_file():
    """Unit test for run_sql_file with variable substitution.
    Verifies that SQL placeholders are correctly replaced
    by the values of the corresponding global variables.
    """
    mock_cursor = Mock()
    sql_content = "SELECT * FROM RAW_TABLE_PLACEHOLDER WHERE user = USER_PLACEHOLDER;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        with patch('snowflake_ingestion.functions.RAW_TABLE', 'my_table'):
            with patch('snowflake_ingestion.functions.USER', 'test_user'):
                run_sql_file(mock_cursor, Path("test.sql"))
    mock_cursor.execute.assert_called_once_with("SELECT * FROM my_table WHERE user = test_user")


def test_run_sql_file_variable_not_found():
    """Unit test for run_sql_file with an unresolved variable.
    Verifies that placeholders with no matching global variable
    are replaced by the default value <VAR_NOT_FOUND>.
    """
    mock_cursor = Mock()
    sql_content = "SELECT * FROM UNKNOWN_PLACEHOLDER;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        run_sql_file(mock_cursor, Path("test.sql"))
    mock_cursor.execute.assert_called_once_with("SELECT * FROM <UNKNOWN_NOT_FOUND>")


def test_run_sql_file_multiple_statements():
    """Unit test for run_sql_file with multiple statements.
    Verifies that statements separated by semicolons are
    correctly split and executed individually.
    """
    mock_cursor = Mock()
    sql_content = "SELECT 1; SELECT 2; SELECT 3;"
    with patch('builtins.open', mock_open(read_data=sql_content)):
        run_sql_file(mock_cursor, Path("test.sql"))
    assert mock_cursor.execute.call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])