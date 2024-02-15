from database.repositories.customer_repository_abc import CustomerRepositoryABC
from database.repositories.base_repository import BaseRepository
from typing import Optional
from database.exceptions.exceptions import DatabaseError

class CustomerRepository(CustomerRepositoryABC, BaseRepository):
    
    def get_all_customers(self) -> list[Optional[tuple]]:
        try:
            with self._db_connection as cursor:
                customers: list[tuple] = cursor.execute('SELECT * FROM Customer;').fetchall()
                if not customers:
                    return []
                else:
                    return customers
        except DatabaseError as e:
            print(f"CustomerRepository.get_all_customers() Error: {e}")
            raise DatabaseError("Error durning getting all customers occured.")

    def update_customer_amount_value(self, customer_id: int, amount_value: int) -> None:
        try:
            with self._db_connection as cursor:
                cursor.execute(f'UPDATE Customer SET amount = {amount_value} WHERE ID = {customer_id};')
        except DatabaseError as e:
            print(f"CustomerRepository.update_customer_amount_value() Error: {e}")
            raise DatabaseError("Error during updating customer amount value occured.")