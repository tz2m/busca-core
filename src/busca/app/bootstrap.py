# busca/app/bootstrap.py
from pathlib import Path
import os
import yaml

from dotenv import load_dotenv
from sqlalchemy import Engine, inspect, text
from dependency_injector import providers

from busca.app.config_loader import load_nota_ri_db_config
from busca.domains.nota_ri.repository.db.model.nota_ri_sql import BaseNotaRi
from busca.domains.nota_ri.repository.db.model.nota_ri_sql_trigger import set_nota_ri_tigger
from busca.app.container import Container

load_dotenv()


def bootstrap() -> Container:
    container = Container()

    load_dotenv()
    env = os.getenv("BUSCA_ENV", "dev")

    BUSCA_DATA = Path(
        os.getenv("BUSCA_DATA", Path(__file__).resolve().parents[3])
    )

    config_path = BUSCA_DATA / "config.yml"

    with open(config_path) as f:
        raw_config = yaml.safe_load(f)

    container.config.from_dict(raw_config)

    # 🔥 resolve config tipada respeitando BUSCA_ENV
    db_config, drop_all = load_nota_ri_db_config(str(config_path))

    # ✅ override correto
    container.nota_ri_database_config.override(
        providers.Object(db_config)
    )

    container.nota_ri_drop_all.override(
        providers.Object(drop_all)
    )

    # agora isso funciona
    engine_nota_ri = container.engine_nota_ri()

    schema_nota_ri(engine_nota_ri, drop_all, env)

    container.wire(
        modules=[
            "busca.interface.api.count_routes",
            "busca.interface.api.health_routes",
            "busca.interface.api.search_routes",
        ]
    )

    return container



def schema_nota_ri(engine: Engine, drop_all: bool, env: str):
    def is_blank_db(eng: Engine) -> bool:
        with eng.connect() as connection:
            inspector = inspect(connection)
            return len(inspector.get_table_names()) == 0

    def init_db(eng: Engine):
        set_nota_ri_tigger()
        BaseNotaRi.metadata.create_all(eng)


    if env == "prod" and drop_all:
        raise RuntimeError("drop_all jamais permitido em produção")

    if drop_all:
        BaseNotaRi.metadata.drop_all(engine)

    if is_blank_db(engine):
        init_db(engine)
