from sqlite3 import connect, Connection, Cursor
from database.exceptions.exceptions import DatabaseError
from typing import Generator
from contextlib import contextmanager
from database.connection_manager.connection_manager_abc import ConnectionManagerABC

class ConnectionManager(ConnectionManagerABC):
    def __init__(self, db_path: str):
        self.db_path: str = db_path

    @contextmanager
    def get_connection(self) -> Generator[Cursor, None, None]:
        connection: Connection = connect(self.db_path)
        try:
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except DatabaseError as e:
            print(f"ConnectionManager.get_connection() Error: {e}")
            connection.rollback()
        finally:
            connection.close()

