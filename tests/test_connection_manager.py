from unittest.mock import patch
from database.connection_manager.connection_manager import ConnectionManager 
from database.exceptions.exceptions import DatabaseError

@patch('database.connection_manager.connection_manager.connect')  
def test_get_connection_success(mock_connect):
    mock_connection = mock_connect.return_value

    manager = ConnectionManager("test_db_path")
    with manager.get_connection() as cursor:
        pass

    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()


@patch('database.connection_manager.connection_manager.connect')  
def test_get_connection_error(mock_connect):
    mock_connection = mock_connect.return_value
    mock_cursor = mock_connection.cursor.return_value
    mock_cursor.execute.side_effect = DatabaseError("Test error")

    manager = ConnectionManager("test_db_path")
    with manager.get_connection() as cursor:
        cursor.execute("SELECT 1")

    mock_connection.rollback.assert_called_once()
    mock_connection.close.assert_called_once()
