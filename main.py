from program.program import Program
from database.repositories.repositories_factory import RepositoriesFactory
from database.connection_manager.connection_manager import ConnectionManager


def main() -> None:
    try:
        connection_manager: ConnectionManager = ConnectionManager(
            db_path='customer.db'
        )

        repositories_factory: RepositoriesFactory = RepositoriesFactory()
        
        program: Program = Program(
            repositories_factory=repositories_factory,
            connection_manager=connection_manager,
        )
        program.start_program()
    except Exception as e:
        print(f"main() error: {e}")

if __name__ == '__main__':
    main()