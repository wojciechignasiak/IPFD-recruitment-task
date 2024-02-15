from program.program_abc import ProgramABC
from database.connection_manager.connection_manager_abc import ConnectionManagerABC
from database.repositories.customer_repository_abc import CustomerRepositoryABC
from database.repositories.repositories_factory_abc import RepositoriesFactoryABC
from database.exceptions.exceptions import DatabaseError
from models.customer_model import CustomerModel
from typing import Optional
from program.exceptions import AttemptsExceeded

class Program(ProgramABC):
    
    def __init__(self, repositories_factory: RepositoriesFactoryABC, connection_manager: ConnectionManagerABC) -> None:
        self.__repositories_factory: RepositoriesFactoryABC = repositories_factory
        self.__connection_manager: ConnectionManagerABC = connection_manager

    def start_program(self) -> None:
        number_of_attempts: int = 0
        while number_of_attempts<3:
            try:
                customer_repository: CustomerRepositoryABC = self.__repositories_factory.get_customer_repository(
                    self.__connection_manager.get_connection()
                )
                customers: list[Optional[tuple]] = customer_repository.get_all_customers()
                if not customers:
                    print("\nNo customers in database. Closing program...")
                    exit()
                
                customers = self._convert_customers_tuple_to_customers_model(customers)
                self._print_customers(customers)
                print("Menu:\n1. add\n2. substract\n")
                menu_input: str = input("Insert option: ")

                match menu_input:
                    case "1":
                        self._add_option(customers=customers)
                        number_of_attempts = 0
                    case "2":
                        self._substract_option(customers=customers)
                        number_of_attempts = 0
                    case _:
                        print(f"Invalid option. Number of attempts {number_of_attempts + 1}/3")
                        if number_of_attempts == 2:
                            raise AttemptsExceeded()
                        number_of_attempts += 1

            except KeyboardInterrupt:
                print("\nKeyboard Interrupted. Closing program...")
                exit()
            except AttemptsExceeded:
                print("\nAttempts exceeded. Closing program...")
                exit()
            except DatabaseError as e:
                print(f"\n{e} Closing program...")
                exit()

    def _add_option(self, customers: list[CustomerModel]) -> bool:
        try:
            number_of_attempts: int = 0
            while number_of_attempts<3:
                customer_id: int = self._get_and_verify_customer_id()
                customer: list[Optional[CustomerModel]] = self._is_customer_with_provided_id_in_list(
                    customer_models=customers,
                    customer_id=customer_id
                )
                if not customer:
                    print(f"Customer with provided ID do not exists. Provide correct ID. Number of attempts {number_of_attempts + 1}/3")
                    if number_of_attempts == 2:
                        raise AttemptsExceeded()
                    number_of_attempts += 1
                else:
                    break
            
            amount: int = self._get_and_verify_amount_value()
            
            print(f"Simulating amount value after changes for customer with ID {customer[0].id}:")
            print(f"Old amount: {customer[0].amount}")
            print(f"New amount: {customer[0].amount + amount}")

            decision: bool = self._confirm_changes()
            match decision:
                case True:
                    customer[0].amount += amount
                    print(customer[0])
                    customer_repository = self.__repositories_factory.get_customer_repository(
                        self.__connection_manager.get_connection()
                    )
                    customer_repository.update_customer_amount_value(
                        customer_id=customer[0].id,
                        amount_value=customer[0].amount
                    )
                    print("Amount value updated successfully.")
                    return True
                case False:
                    print("Changes canceled.")
                    return False
        except DatabaseError as e:
            print(f"\n{e} Closing program...")
            exit()
        except AttemptsExceeded:
            print("\nAttempts exceeded. Closing program...")
            exit()

    def _substract_option(self, customers: list[CustomerModel]) -> bool:
        try:
            number_of_attempts: int = 0
            while number_of_attempts<3:
                customer_id: int = self._get_and_verify_customer_id()
                customer: list[Optional[CustomerModel]] = self._is_customer_with_provided_id_in_list(
                    customer_models=customers,
                    customer_id=customer_id
                )
                if not customer:
                    print(f"Customer with provided ID do not exists. Provide correct ID. Number of attempts {number_of_attempts + 1}/3")
                    if number_of_attempts == 2:
                        raise AttemptsExceeded()
                    number_of_attempts += 1
                else:
                    break

            number_of_attempts: int = 0
            while number_of_attempts<3:
                amount: int = self._get_and_verify_amount_value()

                if customer[0].amount >= amount:
                    print(f"Simulating amount value after changes for customer with ID {customer[0].id}:")
                    print(f"Old amount: {customer[0].amount}")
                    print(f"New amount: {customer[0].amount - amount}")
                
                    decision: bool = self._confirm_changes()
                    match decision:
                        case True:
                            customer[0].amount -= amount
                            customer_repository = self.__repositories_factory.get_customer_repository(
                                self.__connection_manager.get_connection()
                            )
                            customer_repository.update_customer_amount_value(
                                customer_id=customer_id,
                                amount_value=customer[0].amount
                            )
                            print("Amount value updated successfully.")
                            return True
                            
                        case False:
                            print("Changes canceled.")
                            return False
                else:
                    print(f"Amount value would be less than 0. Provide propper value. Number of attempts {number_of_attempts + 1}/3")
                    if number_of_attempts == 2:
                        raise AttemptsExceeded()
                    number_of_attempts += 1
        except DatabaseError as e:
            print(f"\n{e} Closing program...")
            exit()
        except AttemptsExceeded:
            print("\nAttempts exceeded. Closing program...")
            exit()

    def _print_customers(self, customers: list[CustomerModel]) -> None:
        print("Customers in database:")
        print("ID\tName\tAmount")
        for customer in customers:
            print(customer.id , customer.name , customer.amount)

    def _convert_customers_tuple_to_customers_model(self, customers: list[tuple]) -> list[CustomerModel]:
        return [CustomerModel.from_tuple(customer) for customer in customers]

    def _get_and_verify_customer_id(self) -> int:
        number_of_attempts: int = 0
        while number_of_attempts<3:
            try:
                customer_id: str = input("Insert customer ID: ")
                return int(customer_id)
            except ValueError:
                
                print(f"Invalid customer ID, provide customer ID in correct int format. Number of attempts {number_of_attempts + 1}/3")
                if number_of_attempts == 2:
                    print("\nNumber of attempts exceeded. Closing program...")
                    exit()

                number_of_attempts += 1
                continue
            except KeyboardInterrupt:
                print("\nKeyboard Interrupted. Closing program...")
                exit()

    def _get_and_verify_amount_value(self) -> int:
        number_of_attempts: int = 0
        while number_of_attempts<3:
            try:
                amount: str = input("Insert amount: ")
                return int(amount)
            except ValueError:
                print(f"Invalid amount, provide amount in correct int format. Number of attempts {number_of_attempts + 1}/3")
                if number_of_attempts == 2:
                    print("\nNumber of attempts exceeded. Closing program...")
                    exit()
                number_of_attempts += 1
                continue
            except KeyboardInterrupt:
                print("\nKeyboard Interrupted. Closing program...")
                exit()

    def _is_customer_with_provided_id_in_list(self, customer_models: list[CustomerModel], customer_id: int) -> list[Optional[CustomerModel]]:
        customer_model: list[Optional[CustomerModel]] = [customer_model for customer_model in customer_models if customer_model.id == customer_id]
        return customer_model
    
    def _confirm_changes(self) -> bool:
        number_of_attempts: int = 0
        while number_of_attempts<3:
            try:
                confirm: str = input("Confirm changes? (y/n): ")
                match confirm:
                    case "y":
                        return True
                    case "n":
                        return False
                    case _:
                        print(f"Invalid option, provide y or n. Number of attempts {number_of_attempts + 1}/3")
                        if number_of_attempts == 2:
                            raise AttemptsExceeded()
                        number_of_attempts += 1
                        continue
            except KeyboardInterrupt:
                print("\nKeyboard Interrupted. Closing program...")
                exit()
            except AttemptsExceeded:
                print("\nNumber of attempts exceeded. Closing program...")
                exit()