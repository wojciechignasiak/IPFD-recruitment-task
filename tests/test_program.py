from unittest.mock import patch, Mock
from unittest import mock
from program.program import Program
from models.customer_model import CustomerModel
from program.exceptions import AttemptsExceeded
from database.exceptions.exceptions import DatabaseError
import pytest

@patch('builtins.input', return_value='y')
def test_confirm_changes_y(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    assert program._confirm_changes() == True

@patch('builtins.input', return_value='n')
def test_confirm_changes_n(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    assert program._confirm_changes() == False

@patch('builtins.input', side_effect=["invalid"] * 3)
def test_confirm_changes_invalid_option(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout:
            program._confirm_changes()
            assert mock_stdout.called
            assert "\nNumber of attempts exceeded. Closing program..." in mock_stdout.getvalue()

@patch('builtins.input', side_effect=KeyboardInterrupt)
def test_confirm_changes_keyboard_interrupt(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout, mock.patch('sys.exit'):
            program._confirm_changes()
            assert mock_stdout.called
            assert "\nKeyboard Interrupted. Closing program..." in mock_stdout.getvalue()

@patch('builtins.input', return_value='1')
def test_get_and_verify_amount_value_success(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    assert program._get_and_verify_amount_value() == 1

@patch('builtins.input', side_effect=["invalid"] * 3)
def test_get_and_verify_amount_value_invalid_value(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout:
            program._get_and_verify_amount_value()
            assert mock_stdout.called
            assert "\nNumber of attempts exceeded. Closing program..." in mock_stdout.getvalue()

@patch('builtins.input', side_effect=KeyboardInterrupt)
def test_get_and_verify_amount_value_keyboard_interrupt(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout, mock.patch('sys.exit'):
            program._get_and_verify_amount_value()
            assert mock_stdout.called
            assert "\nKeyboard Interrupted. Closing program..." in mock_stdout.getvalue()


@patch('builtins.input', return_value='1')
def test_get_and_verify_customer_id_success(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    assert program._get_and_verify_customer_id() == 1

@patch('builtins.input', side_effect=["invalid"] * 3)
def test_get_and_verify_customer_id_invalid_value(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout:
            program._get_and_verify_customer_id()
            assert mock_stdout.called
            assert "\nNumber of attempts exceeded. Closing program..." in mock_stdout.getvalue()

@patch('builtins.input', side_effect=KeyboardInterrupt)
def test_get_and_verify_customer_id_keyboard_interrupt(
    mock_input,
    mock_repositories_factory,
    mock_connection_manager):
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout, mock.patch('sys.exit'):
            program._get_and_verify_customer_id()
            assert mock_stdout.called
            assert "\nKeyboard Interrupted. Closing program..." in mock_stdout.getvalue()


def test_substract_option_success(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=True)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    assert program._substract_option(customers=[customer_model]) == True


def test_substract_option_not_confirmed(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=False)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    assert program._substract_option(customers=[customer_model]) == False


def test_substract_option_to_big_amount_value_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=101)
    program._confirm_changes = Mock(return_value=False)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    with pytest.raises(SystemExit):
        with pytest.raises(AttemptsExceeded):
            with mock.patch('sys.stdout') as mock_stdout:
                program._substract_option(customers=[customer_model])
                assert mock_stdout.called
                assert "\nAttempts exceeded. Closing program..." in mock_stdout.getvalue()

def test_substract_option_no_customer_with_provided_id_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=False)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[])
    
    with pytest.raises(SystemExit):
        with pytest.raises(AttemptsExceeded):
            with mock.patch('sys.stdout') as mock_stdout:
                program._substract_option(customers=[customer_model])
                assert mock_stdout.called
                assert "\nAttempts exceeded. Closing program..." in mock_stdout.getvalue()


def test_substract_option_database_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_customer_repository.update_customer_amount_value.side_effect = DatabaseError("Database error occured.")
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=True)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    with pytest.raises(SystemExit):
        with pytest.raises(DatabaseError):
            with mock.patch('sys.stdout') as mock_stdout:
                program._substract_option(customers=[customer_model]) 
                assert mock_stdout.called
                assert "\nDatabase error occured. Closing program..." in mock_stdout.getvalue()

def test_add_option_success(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):
    
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=True)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    assert program._add_option(customers=[customer_model]) == True

def test_add_option_not_confirmed(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):
    
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=False)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    assert program._add_option(customers=[customer_model]) == False

def test_add_option_database_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):
    
    mock_customer_repository.update_customer_amount_value.side_effect = DatabaseError("Database error occured.")
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=True)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[customer_model])
    
    with pytest.raises(SystemExit):
        with pytest.raises(DatabaseError):
            with mock.patch('sys.stdout') as mock_stdout:
                program._add_option(customers=[customer_model]) 
                assert mock_stdout.called
                assert "\nDatabase error occured. Closing program..." in mock_stdout.getvalue()

def test_add_option_no_customer_with_provided_id_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):
    
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    program._get_and_verify_customer_id = Mock(return_value=1)
    program._get_and_verify_amount_value = Mock(return_value=100)
    program._confirm_changes = Mock(return_value=True)
    program._is_customer_with_provided_id_in_list = Mock(return_value=[])
    
    with pytest.raises(SystemExit):
        with pytest.raises(AttemptsExceeded):
            with mock.patch('sys.stdout') as mock_stdout:
                program._add_option(customers=[customer_model]) 
                assert mock_stdout.called
                assert "\nAttempts exceeded. Closing program..." in mock_stdout.getvalue()


def test_convert_customers_tuple_to_customers_model_success(
    mock_repositories_factory,
    mock_connection_manager):
    
    customer_model = CustomerModel(
                id=1,
                name="John Doe",
                amount=100
            )
    customer_list_tuple: list[tuple] = [(1, "John Doe", 100)]
    
    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )
    assert program._convert_customers_tuple_to_customers_model(customers=customer_list_tuple) == [customer_model]

@patch('builtins.input', side_effect=KeyboardInterrupt)
def test_start_program_keyboard_interrupt(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository
    mock_customer_repository.get_all_customers.return_value = [(1, "John Doe", 100)]

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )

    with pytest.raises(SystemExit):
        with pytest.raises(KeyboardInterrupt):
            with mock.patch('sys.stdout') as mock_stdout:
                program.start_program()
                assert mock_stdout.called
                assert "\nKeyboard Interrupted. Closing program..." in mock_stdout.getvalue()

def test_start_program_no_customers_in_database(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository
    mock_customer_repository.get_all_customers.return_value = []

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )

    with pytest.raises(SystemExit):
        with mock.patch('sys.stdout') as mock_stdout:
            program.start_program()
            assert mock_stdout.called
            assert "No customers in database. Closing program..." in mock_stdout.getvalue()


def test_start_program_database_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_customer_repository.get_all_customers.side_effect = DatabaseError("Database error occured.")
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )

    with pytest.raises(SystemExit):
        with pytest.raises(DatabaseError):
            with mock.patch('sys.stdout') as mock_stdout:
                program.start_program()
                assert mock_stdout.called
                assert "\nDatabase error occured. Closing program..." in mock_stdout.getvalue()

@patch('builtins.input', side_effect=["invalid"] * 3)
def test_start_program_invalid_error(
    mock_repositories_factory,
    mock_connection_manager,
    mock_customer_repository):

    mock_customer_repository.get_all_customers.return_value = [(1, "John Doe", 100)]
    mock_repositories_factory.get_customer_repository.return_value = mock_customer_repository

    program = Program(
        mock_repositories_factory,
        mock_connection_manager
    )

    with pytest.raises(SystemExit):
        with pytest.raises(AttemptsExceeded):
            with mock.patch('sys.stdout') as mock_stdout:
                program.start_program()
                assert mock_stdout.called
                assert "\nAttempts exceeded. Closing program..." in mock_stdout.getvalue()