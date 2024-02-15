import pytest
from database.repositories.customer_repository import CustomerRepository
from database.exceptions.exceptions import DatabaseError

def test_get_all_customers_empty_result(mock_db_connection):
    mock_cursor = mock_db_connection.__enter__.return_value
    mock_cursor.execute.return_value.fetchall.return_value = []
    repository = CustomerRepository(mock_db_connection)
    result = repository.get_all_customers()
    
    assert isinstance(result, list)
    assert result == []

def test_get_all_customers_result(mock_db_connection):
    mock_cursor = mock_db_connection.__enter__.return_value
    mock_cursor.execute.return_value.fetchall.return_value = [
        (1, 'John Doe', 1000),
        (2, 'Jane Doe', 2000),
        (3, 'Jack Doe', 3000)
    ]
    repository = CustomerRepository(mock_db_connection)
    result = repository.get_all_customers()

    assert isinstance(result, list)
    assert isinstance(result[0], tuple)
    assert len(result) == 3
    assert result[0] == (1, 'John Doe', 1000)

def test_get_all_customers_error(mock_db_connection):
    mock_cursor = mock_db_connection.__enter__.return_value
    mock_cursor.execute.side_effect = DatabaseError("Error occured")
    repository = CustomerRepository(mock_db_connection)

    with pytest.raises(DatabaseError):
        repository.get_all_customers()

def test_update_customer_amount_value_success(mock_db_connection):
    mock_cursor = mock_db_connection.__enter__.return_value
    repository = CustomerRepository(mock_db_connection)
    repository.update_customer_amount_value(
        1,
        100
    )
    mock_cursor.execute.assert_called_once_with('UPDATE Customer SET amount = 100 WHERE ID = 1;')

def test_update_customer_amount_value_error(mock_db_connection):
    mock_cursor = mock_db_connection.__enter__.return_value
    mock_cursor.execute.side_effect = DatabaseError("Error occured")

    repository = CustomerRepository(mock_db_connection)

    with pytest.raises(DatabaseError):
        repository.update_customer_amount_value(
            1,
            100
        )
