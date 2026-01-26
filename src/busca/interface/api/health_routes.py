# interface/api/health_routes.py
from fastapi import APIRouter, Depends, Path, HTTPException
from dependency_injector.wiring import inject, Provide

from busca.app.container import Container
from busca.app.services.health_check_resolver import HealthCheckResolver

router = APIRouter()


@router.get("/{domain}/health")
@inject
def health(
    domain: str = Path(..., description="Domain name (nota-ri, sinpet, etc.)"),
    resolver: HealthCheckResolver = Depends(
        Provide[Container.health_check_resolver]
    ),
):
    try:
        health_check = resolver.resolve(domain)
        return health_check.check()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
