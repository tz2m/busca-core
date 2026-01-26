from abc import ABC, abstractmethod


class CountUseCase(ABC):
    @abstractmethod
    def execute(self):
        ...
