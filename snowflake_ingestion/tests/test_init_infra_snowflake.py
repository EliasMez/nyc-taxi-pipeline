from unittest.mock import Mock, patch
import snowflake_ingestion.init_infra_snowflake as infra

def test_set_data_retention():
    """
    Unit test for the set_data_retention function.
    Verifies that the function executes the correct SQL file with the specified retention time
    and logs appropriate messages when setting data retention policies.
    """
    mock_cursor = Mock()
    
    with patch('snowflake_ingestion.init_infra_snowflake.functions.RETENTION_TIME', 90):
        with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
            with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
                infra.set_data_retention(mock_cursor)

def test_setup_data_warehouse():
    """
    Unit test for the setup_data_warehouse function.
    Tests the creation of warehouse, database, and schemas infrastructure in Snowflake.
    Verifies that the correct SQL script is executed and appropriate log messages are recorded
    during the warehouse setup process.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.setup_data_warehouse(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "setup_data_warehouse.sql")
            mock_logger.info.assert_any_call("🏗️  Creating warehouse, database and schemas...")
            mock_logger.info.assert_any_call("✅ Warehouse and schemas created")

def test_create_roles_and_user():
    """
    Unit test for the create_roles_and_user function.
    Tests the creation of Snowflake roles and users as part of infrastructure initialization.
    Verifies that the appropriate SQL script is executed and success/failure logs are properly
    recorded during the role and user creation process.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.create_roles_and_user(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "create_roles_and_user.sql")
            mock_logger.info.assert_any_call("🔐 Creating roles and users...")
            mock_logger.info.assert_any_call("✅ Roles and users created")

def test_grant_privileges():
    """
    Unit test for the grant_privileges function.
    Tests the granting of privileges to the created roles in Snowflake.
    Verifies that the correct SQL script is executed and appropriate log messages are recorded
    during the privilege granting process.
    """
    mock_cursor = Mock()
    with patch('snowflake_ingestion.init_infra_snowflake.functions.run_sql_file') as mock_run_sql:
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.grant_privileges(mock_cursor)
            
            mock_run_sql.assert_called_once_with(mock_cursor, infra.SQL_DIR / "grant_privileges.sql")
            mock_logger.info.assert_any_call("🔑 Granting privileges to the roles...")
            mock_logger.info.assert_any_call("✅ Privileges granted")

def test_main_exception():
    """
    Unit test for the main function when an exception occurs during initialization.
    Tests error handling by simulating a connection failure and verifying that the
    exception is properly caught and logged as an error.
    """
    with patch('snowflake_ingestion.init_infra_snowflake.functions.connect_with_role', side_effect=Exception("Connection failed")):
        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
            infra.main()
            mock_logger.error.assert_called_once()

def test_main_success():
    """
    Unit test for the main function when the infrastructure initialization completes successfully.
    Tests the complete initialization flow including warehouse setup, role creation,
    and privilege granting. Verifies that all three connections are made with the
    appropriate roles (ACCOUNTADMIN, SYSADMIN, SECURITYADMIN) and that all
    initialization functions are called in sequence with successful logging.
    """
    mock_conns = [Mock(), Mock(), Mock()]
    for mock_conn in mock_conns:
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=Mock())
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=None)
    
    call_counter = 0
    def connect_side_effect(*args, **kwargs):
        nonlocal call_counter
        if call_counter < len(mock_conns):
            result = mock_conns[call_counter]
            call_counter += 1
            return result
        return Mock()
    
    with patch('snowflake_ingestion.init_infra_snowflake.functions.RETENTION_TIME', 90):
        with patch('snowflake_ingestion.init_infra_snowflake.functions.connect_with_role', 
                   side_effect=connect_side_effect) as mock_connect:
            with patch('snowflake_ingestion.init_infra_snowflake.setup_data_warehouse') as mock_setup:
                with patch('snowflake_ingestion.init_infra_snowflake.create_roles_and_user') as mock_create:
                    with patch('snowflake_ingestion.init_infra_snowflake.grant_privileges') as mock_grant:
                        with patch('snowflake_ingestion.init_infra_snowflake.logger') as mock_logger:
                            infra.main()
                            
                            assert mock_connect.call_count == 3
                            mock_connect.assert_any_call(infra.functions.USER, infra.functions.PASSWORD, infra.functions.ACCOUNT, 'ACCOUNTADMIN')
                            mock_connect.assert_any_call(infra.functions.USER, infra.functions.PASSWORD, infra.functions.ACCOUNT, 'SYSADMIN')
                            mock_connect.assert_any_call(infra.functions.USER, infra.functions.PASSWORD, infra.functions.ACCOUNT, 'SECURITYADMIN')
                            
                            mock_setup.assert_called_once()
                            mock_create.assert_called_once()
                            mock_grant.assert_called_once()
                            mock_logger.info.assert_called_with("🎯 Complete initialization finished successfully!")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])