# busca/app/bootstrap.py
from pathlib import Path
import os
import yaml

from dotenv import load_dotenv
from sqlalchemy import Engine, inspect, text
from dependency_injector import providers
from sqlalchemy.dialects.postgresql import Any

from busca.core.entity.domain_config import DatabaseConfig
from busca.domains.nota_ri.repository.db.model.nota_ri_sql import BaseNotaRi
from busca.domains.nota_ri.repository.db.model.nota_ri_sql_trigger import set_nota_ri_tigger
from busca.domains.material.repository.db.model.material_sql import BaseMaterial
from busca.domains.material.repository.db.model.material_sql_trigger import set_material_trigger
from busca.app.container import Container

load_dotenv()


def bootstrap() -> Container:
    container = Container()

    BUSCA_DATA = Path(
        os.getenv("BUSCA_DATA", Path(__file__).resolve().parents[3])
    )

    config_path = BUSCA_DATA / "config.yml"

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    container.config.from_dict(raw_config)
    container.nota_ri_database_config.override(
        providers.Object(DatabaseConfig(**container.config.nota_ri.database().get(os.getenv("BUSCA_ENV", "dev"))))
    )
    init_schema(container.engine_nota_ri(), container.nota_ri_database_config().drop_all, BaseNotaRi,
                set_nota_ri_tigger)

    container.material_database_config.override(
        providers.Object(DatabaseConfig(**container.config.material.database().get(os.getenv("BUSCA_ENV", "dev"))))
    )
    init_schema(container.engine_material(), container.material_database_config().drop_all, BaseMaterial,
                set_material_trigger)

    container.wire(
        modules=[
            "busca.interface.api.count_routes",
            "busca.interface.api.health_routes",
            "busca.interface.api.search_routes",
        ]
    )

    return container


def init_schema(engine: Engine, drop_all: bool, entity: Any, tigger_setter):
    def is_blank_db(eng: Engine) -> bool:
        with eng.connect() as connection:
            inspector = inspect(connection)
            return len(inspector.get_table_names()) == 0

    def init_db(eng: Engine):
        tigger_setter()
        entity.metadata.create_all(eng)

    if os.getenv("BUSCA_ENV", "dev") == "prod" and drop_all:
        raise RuntimeError("drop_all jamais permitido em produção")

    if drop_all:
        entity.metadata.drop_all(engine)

    if is_blank_db(engine):
        init_db(engine)
