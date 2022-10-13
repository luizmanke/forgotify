from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker


class ItemIsNotPersistedError(Exception):
    pass


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

    def search(self, table: Any) -> List[Any]:
        return (
            self._session
            .query(table)
            .all()
        )

    def count(self, table: Any) -> int:
        items = self.search(table)
        return len(items)

    def delete(self, item: Any):
        try:
            self._session.delete(item)
            self._session.commit()
        except InvalidRequestError:
            raise ItemIsNotPersistedError()
