from abc import abstractmethod, ABC
from database.repositories.customer_repository_abc import CustomerRepositoryABC

class RepositoriesFactoryABC(ABC):

    @abstractmethod
    def get_customer_repository(self, db_connection) -> CustomerRepositoryABC:
        ...