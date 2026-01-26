from typing import List, Any
from busca.core import SearchRepository
from busca.domains.sinpet.search_service import search_with_highlight
from busca.core import Session

class SinpetSearchAdapter(SearchRepository):
    def search(self, query: str, limit: int = 10, offset: int = 0) -> List[Any]:
        # generic search interface
        # Our specific implementation uses 'session' and 'search_text'
        # It handles session internally? No, search_with_highlight takes session.
        with Session() as session:
             return search_with_highlight(query, session, limit)
