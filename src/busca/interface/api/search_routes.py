from fastapi import APIRouter, Depends, HTTPException, Query, Path
from dependency_injector.wiring import inject, Provide

from busca.app.container import Container
from busca.app.services.search_use_case_resolver import SearchUseCaseResolver

router = APIRouter()


@router.get(
    "/{domain}/search",
    summary="Busca FTS por domínio",
    description="Executa busca full-text search no domínio informado (ex: nota_ri, sinpet)",
)
@inject
def search(
    domain: str = Path(..., description="Domain name (nota_ri, sinpet, etc.)"),
    q: str = Query(..., min_length=2, description="Texto da busca"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    resolver: SearchUseCaseResolver = Depends(
        Provide[Container.search_use_case_resolver]
    ),
):
    try:
        use_case = resolver.resolve(domain)
        return use_case.execute(q, limit, offset)

    except ValueError as e:
        # domínio inexistente
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # erro inesperado
        raise HTTPException(status_code=500, detail=str(e))
