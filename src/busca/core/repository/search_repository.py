from typing import Protocol, List
from busca.app.dto.search_result_dto import SearchResultDTO


class SearchRepository(Protocol):
    def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SearchResultDTO]:
        ...
