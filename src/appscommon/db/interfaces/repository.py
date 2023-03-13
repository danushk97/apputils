from abc import ABC, abstractmethod
from typing import Any

from appscommon.domain.models.basemodel import BaseModel


class AbstractRepository(ABC):
    _session: Any  # Any DB session object.

    def add(self, entity: BaseModel):
        self._session.add(entity)

    @abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError
