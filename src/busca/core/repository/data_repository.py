from abc import ABC, abstractmethod
from typing import List, Any, Iterator


class DataRepository(ABC):
    @abstractmethod
    def extract(self, current_state: List[Any]) -> Iterator[Any]:
        pass

    @abstractmethod
    def get_current_state(self) -> List[Any]:
        pass

    @abstractmethod
    def save(self, item: Any):
        pass

    @abstractmethod
    def size(self):
        pass
