# interface/api/count_routes.py
from fastapi import APIRouter, Depends, Path, HTTPException
from dependency_injector.wiring import inject, Provide

from busca.app.container import Container
from busca.app.services.count_use_case_resolver import CountUseCaseResolver

router = APIRouter()


@router.get("/{domain}/count")
@inject
def count(
    domain: str = Path(..., description="Domain name (nota-ri, sinpet, etc.)"),
    resolver: CountUseCaseResolver = Depends(
        Provide[Container.count_use_case_resolver]
    ),
):
    try:
        use_case = resolver.resolve(domain)
        return use_case.execute()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
