from typing import Any, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression


class ItemIsNotPersistedError(Exception):
    pass


# some change
class Session:

    def __init__(
        self,
        host: str,
        port: str,
        username: str,
        password: str,
        database: str,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self._create_engine()
        self._create_session()

    def _create_engine(self):
        self._engine = create_engine(
            f"postgresql://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )

    def _create_session(self):
        Session = sessionmaker(self._engine)
        self._session = Session()

    def add(self, item: Any):
        self._session.add(item)
        self._session.commit()

    def update(self, item: Any):
        self._session.commit()

    def search(self, table: Any, condition: Optional[BinaryExpression] = None) -> List[Any]:
        results = self._session.query(table)
        if condition is not None:
            results = results.filter(condition)
        return results.all()

    def count(self, table: Any, condition: Optional[BinaryExpression] = None) -> int:
        items = self.search(table, condition)
        return len(items)

    def delete(self, item: Any):
        try:
            self._session.delete(item)
            self._session.commit()
        except InvalidRequestError:
            raise ItemIsNotPersistedError()
