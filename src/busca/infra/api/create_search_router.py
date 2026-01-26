from fastapi import APIRouter
from typing import List, Any

from busca.core.use_case.search_use_case import SearchUseCase


# Dependency injection needs a way to get the repo.
# We will use app.state.search_repo

def create_search_router(search: SearchUseCase) -> APIRouter:
    router = APIRouter()

    @router.get("/search", response_model=List[Any])
    def search(q: str, limit, offset):
        return search.execute(q, limit, offset)

    return router

