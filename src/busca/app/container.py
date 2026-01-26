# app/container.py
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from busca.app.config_loader import load_nota_ri_db_config
from busca.app.services.count_use_case_resolver import CountUseCaseResolver
from busca.app.services.health_check_resolver import HealthCheckResolver
from busca.app.services.search_use_case_resolver import SearchUseCaseResolver
from busca.app.services.sync_service import SyncService
from busca.core.entity.domain_config import DatabaseConfig
from busca.core.use_case.search_use_case import SearchUseCase

from busca.domains.nota_ri.repository.csv.nota_ri_repository_csv import NotaRIRepositoryCSV
from busca.domains.nota_ri.repository.db.nota_ri_count_use_case import NotaRICountUseCase
from busca.domains.nota_ri.repository.db.nota_ri_health_repository_sql import NotaRIHealthRepository
from busca.domains.nota_ri.repository.db.nota_ri_repository_sql import NotaRIRepositorySql
from busca.domains.nota_ri.repository.db.search_nota_ri_repository_sql import SearchNotaRiRepositorySql


class Container(containers.DeclarativeContainer):
    """Container de injeção de dependências"""
    config = providers.Configuration()

    # 🔥 esses são injetados pelo bootstrap
    nota_ri_database_config = providers.Singleton(lambda: None)
    nota_ri_drop_all = providers.Singleton(lambda: False)

    engine_nota_ri = providers.Singleton(
        create_engine,
        nota_ri_database_config.provided.url,
        pool_pre_ping=True,
        future=True,
    )

    session_factory_nota_ri = providers.Singleton(
        sessionmaker,
        bind=engine_nota_ri,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session_nota_ri = providers.Factory(
        session_factory_nota_ri,
    )

    # --- Repos ---
    nota_ri_repo_sql = providers.Factory(
        NotaRIRepositorySql,
        session=session_nota_ri,
    )

    nota_ri_repo_csv = providers.Factory(
        NotaRIRepositoryCSV,
        file=config.nota_ri.csv.file,
    )

    search_nota_ri_repo = providers.Factory(
        SearchNotaRiRepositorySql,
        session=session_factory_nota_ri,
    )


    # --- Use Cases concretos ---
    count_nota_ri = providers.Factory(
        NotaRICountUseCase,
        repo=nota_ri_repo_sql,
    )
    health_nota_ri = providers.Factory(
        NotaRIHealthRepository,
        engine=engine_nota_ri,
    )

    search_nota_ri_use_case = providers.Factory(
        SearchUseCase,
        repo=search_nota_ri_repo,
    )

    # --- Mapa de domínios ---
    count_use_case_map = providers.Dict(
        nota_ri=count_nota_ri,
    )
    health_repo_map = providers.Dict(
        nota_ri=health_nota_ri,
    )

    search_use_case_map = providers.Dict(
        nota_ri=search_nota_ri_use_case,
    )




    # --- Resolver (fachada application) ---
    count_use_case_resolver = providers.Factory(
        CountUseCaseResolver,
        use_cases=count_use_case_map,
    )
    health_check_resolver = providers.Factory(
        HealthCheckResolver,
        repos=health_repo_map,
    )

    nota_ri_sync_service = providers.Factory(
        SyncService,
        orig_repo=nota_ri_repo_csv,
        dest_repo=nota_ri_repo_sql
    )

    search_use_case_resolver = providers.Factory(
        SearchUseCaseResolver,
        use_cases=search_use_case_map,
    )