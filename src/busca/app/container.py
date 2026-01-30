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

from busca.domains.material.repository.db.material_count_use_case import MaterialCountUseCase
from busca.domains.material.repository.db.material_health_repository_sql import MaterialHealthRepository
from busca.domains.material.repository.db.material_repository_sql import MaterialRepositorySql
from busca.domains.material.repository.db.search_material_repository_sql import SearchMaterialRepositorySql
from busca.domains.material.repository.sqlite.material_repository_sqlite import MaterialRepositorySqlite


class Container(containers.DeclarativeContainer):
    """Container de injeção de dependências"""
    config = providers.Configuration()

    # 🔥 esses são injetados pelo bootstrap
    nota_ri_database_config = providers.Singleton(lambda: None)

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

    # ========== MATERIAL DOMAIN ==========

    # 🔥 injetados pelo bootstrap
    material_database_config = providers.Singleton(lambda: None)

    engine_material = providers.Singleton(
        create_engine,
        material_database_config.provided.url,
        pool_pre_ping=True,
        future=True,
    )

    session_factory_material = providers.Singleton(
        sessionmaker,
        bind=engine_material,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    session_material = providers.Factory(
        session_factory_material,
    )

    # --- Repos ---
    material_repo_sql = providers.Factory(
        MaterialRepositorySql,
        session=session_material,
    )

    material_repo_sqlite = providers.Factory(
        MaterialRepositorySqlite,
        file=config.material.sqlite.file,
    )

    search_material_repo = providers.Factory(
        SearchMaterialRepositorySql,
        session=session_factory_material,
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

    # --- Material Use Cases ---
    count_material = providers.Factory(
        MaterialCountUseCase,
        repo=material_repo_sql,
    )
    health_material = providers.Factory(
        MaterialHealthRepository,
        engine=engine_material,
    )

    search_material_use_case = providers.Factory(
        SearchUseCase,
        repo=search_material_repo,
    )

    # --- Mapa de domínios ---
    count_use_case_map = providers.Dict(
        nota_ri=count_nota_ri,
        material=count_material,
    )
    health_repo_map = providers.Dict(
        nota_ri=health_nota_ri,
        material=health_material,
    )

    search_use_case_map = providers.Dict(
        nota_ri=search_nota_ri_use_case,
        material=search_material_use_case,
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

    material_sync_service = providers.Factory(
        SyncService,
        orig_repo=material_repo_sqlite,
        dest_repo=material_repo_sql
    )

    search_use_case_resolver = providers.Factory(
        SearchUseCaseResolver,
        use_cases=search_use_case_map,
    )
