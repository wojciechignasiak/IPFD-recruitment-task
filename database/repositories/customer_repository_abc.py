from abc import abstractmethod, ABC
from typing import Optional


class CustomerRepositoryABC(ABC):
    
    @abstractmethod
    def get_all_customers(self) -> list[Optional[tuple]]:
        ...

    @abstractmethod
    def update_customer_amount_value(self, customer_id: int, amount_value: int) -> None:
        ...