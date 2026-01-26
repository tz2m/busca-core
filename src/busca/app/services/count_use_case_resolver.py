# application/services/count_use_case_resolver.py
from typing import Dict

from busca.core.use_case.count_use_case import CountUseCase


class CountUseCaseResolver:
    def __init__(self, use_cases: Dict[str, CountUseCase]):
        self._use_cases = use_cases

    def resolve(self, domain: str) -> CountUseCase:
        try:
            return self._use_cases[domain]
        except KeyError:
            raise ValueError(f"Unknown domain: {domain}")
