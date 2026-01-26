from typing import List

from busca.app.dto.search_result_dto import SearchResultDTO
from busca.core.repository.search_repository import SearchRepository


class SearchUseCase:

    def __init__(self, repo: SearchRepository):
        self.repo = repo

    def execute(self, q: str, limit=10, offset=0) -> List[SearchResultDTO]:
        return self.repo.search(q, limit, offset)
