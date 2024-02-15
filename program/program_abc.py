from abc import ABC, abstractmethod
from models.customer_model import CustomerModel
from typing import Optional


class ProgramABC(ABC):

    @abstractmethod
    def start_program(self):
        ...
    
    @abstractmethod
    def _add_option(self, customers: list[CustomerModel]) -> bool:
        ...

    @abstractmethod
    def _substract_option(self, customers: list[CustomerModel]) -> bool:
        ...

    @abstractmethod
    def _print_customers(self, customers: list[CustomerModel]) -> None:
        ...

    @abstractmethod
    def _convert_customers_tuple_to_customers_model(self, customers: list[tuple]) -> list[CustomerModel]:
        ...

    @abstractmethod
    def _get_and_verify_customer_id(self) -> int:
        ...

    @abstractmethod
    def _get_and_verify_amount_value(self) -> int:
        ...

    @abstractmethod
    def _is_customer_with_provided_id_in_list(self, customer_models: list[CustomerModel], customer_id) -> list[Optional[CustomerModel]]:
        ...

    @abstractmethod
    def _confirm_changes(self) -> bool:
        ...