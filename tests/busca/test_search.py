

from typing import List
from busca.core.repository.search_repository import SearchRepository
from busca.app.dto.search_result_dto import SearchResultDTO

from busca.core.use_case.search_use_case import SearchUseCase


class FakeSearchRepository(SearchRepository):

    def search(self, query: str, limit: int = 10, offset: int = 0) -> List[SearchResultDTO]:
        return [
            SearchResultDTO(
                item={"num_ri": "123"},
                score=0.9,
                highlight="... bomba ..."
            )
        ]

def test_search_use_case():
    uc = SearchUseCase(repo=FakeSearchRepository())

    results = uc.execute("bomba")

    assert len(results) == 1
    assert results[0].score == 0.9
    assert "bomba" in results[0].highlight