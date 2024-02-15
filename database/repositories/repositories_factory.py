from database.repositories.customer_repository import CustomerRepository
from database.repositories.customer_repository_abc import CustomerRepositoryABC
from database.repositories.repositories_factory_abc import RepositoriesFactoryABC 

class RepositoriesFactory(RepositoriesFactoryABC):

    def get_customer_repository(self, db_connection) -> CustomerRepositoryABC:
        return CustomerRepository(db_connection)