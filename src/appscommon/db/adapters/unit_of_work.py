"""
This module holds the unit of work class for sqlalchemy.
"""

from appscommon.db.interfaces.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    """
    Handles and keeps track of all the transaction made with the database and
    also handles the database session.

    Attributes:
        session_factory: A session maker that should return a db session object.
    """
    def __init__(self, session_factory):
        """
        Instantiates the class.
        """
        self._session_factory = session_factory

    def __enter__(self):
        """
        Gets executed when this instance of class is used with "with" statement.
        """
        self._session = self._session_factory()

        return super().__enter__()

    def commit(self) -> None:
        """
        Saves all the changes whcih was made during the current database
        session.
        """
        self._session.commit()

    def flush(self) -> None:
        """
        Saves all the changes whcih was made during the current database
        session.
        """
        self._session.flush()

    def rollback(self) -> None:
        """
        Discards all the changes whcih was made after the latest commit.
        """
        self._session.rollback()

    def end_session(self) -> None:
        """
        Closes the current DB session.
        """
        self._session.close()
