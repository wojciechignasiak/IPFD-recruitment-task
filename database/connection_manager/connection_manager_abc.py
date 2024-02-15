from sqlite3 import Cursor
from typing import Generator
from contextlib import contextmanager
from abc import ABC, abstractmethod



class ConnectionManagerABC(ABC):

    @abstractmethod
    @contextmanager
    def get_connection(self) -> Generator[Cursor, None, None]:
        ...

