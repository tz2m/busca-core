# application/services/health_check_resolver.py
from typing import Dict

from busca.core.repository.health_repository import HealthRepository


class HealthCheckResolver:
    def __init__(self, repos: Dict[str, HealthRepository]):
        self._repos = repos

    def resolve(self, domain: str) -> HealthRepository:
        try:
            return self._repos[domain]
        except KeyError:
            raise ValueError(f"Unknown domain: {domain}")
