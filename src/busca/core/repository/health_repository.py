# infrastructure/health/health_repository.py
from abc import ABC, abstractmethod


class HealthRepository(ABC):
    @abstractmethod
    def check(self) -> dict:
        ...
