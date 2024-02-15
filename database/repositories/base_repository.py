from sqlite3 import Cursor
from typing import Generator

class BaseRepository:
    def __init__(self, db_connection: Generator[Cursor, None, None]):
        self._db_connection: Generator[Cursor, None, None] = db_connection