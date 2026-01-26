# application/services/count_use_case_resolver.py
from typing import Dict

from busca.core.use_case.search_use_case import SearchUseCase


class SearchUseCaseResolver:

    def __init__(self, use_cases: Dict[str, SearchUseCase]):
        self._use_cases = use_cases

    def resolve(self, domain: str) -> SearchUseCase:
        try:
            return self._use_cases[domain]
        except KeyError:
            raise ValueError(f"Unknown domain: {domain}")
