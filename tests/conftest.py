import pytest
from unittest.mock import MagicMock, Mock
from database.repositories.repositories_factory import RepositoriesFactory
from database.repositories.customer_repository import CustomerRepository
from database.connection_manager.connection_manager import ConnectionManager


@pytest.fixture
def mock_db_connection():
    return MagicMock()

@pytest.fixture
def mock_repositories_factory():
    return Mock(spec=RepositoriesFactory)

@pytest.fixture
def mock_customer_repository():
    return Mock(spec=CustomerRepository)

@pytest.fixture
def mock_connection_manager():
    return Mock(spec=ConnectionManager)
