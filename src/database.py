import sqlite3


class Database:
    def __init__(self, path):
        self._path = path

    def __enter__(self):
        self._con = sqlite3.connect(self._path)
        self._create_schema()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._con.close()

    def _create_schema(self):
        pass
