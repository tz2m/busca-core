# Define Config
from fastapi import FastAPI

from busca.app.bootstrap import bootstrap
from busca.app.container import Container

from busca.interface.api.count_routes import router as count_router
from busca.interface.api.health_routes import router as health_router
from busca.interface.api.search_routes import router as search_router


def create_app() -> FastAPI:
    app = FastAPI(title="Busca Core")

    container = bootstrap()
    app.container = container

    app.include_router(count_router, prefix="/api")
    app.include_router(health_router, prefix="/api")
    app.include_router(search_router, prefix="/api")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
