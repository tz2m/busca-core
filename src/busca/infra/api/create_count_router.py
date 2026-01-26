from fastapi import APIRouter
from typing import List, Any

from busca.core.use_case.count_use_case import CountUseCase


# Dependency injection needs a way to get the repo.
# We will use app.state.search_repo

def create_count_router(count: CountUseCase) -> APIRouter:
    router = APIRouter()

    @router.get("/count", response_model=List[Any])
    def count():
        return count.execute()

    return router

