# tests/integration/conftest.py
import os
from pathlib import Path

import pytest
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from busca.app.config_loader import load_nota_ri_db_config
from busca.app.bootstrap import schema_nota_ri, bootstrap


@pytest.fixture(scope="session")
def engine():
    os.environ.setdefault("BUSCA_ENV", "test")

    ROOT = Path(__file__).resolve().parents[2]
    config_path = ROOT / "data" / "config.yml"

    if not config_path.exists():
        raise RuntimeError(f"config.yml não encontrado em: {config_path}")

    db_config, drop_all = load_nota_ri_db_config(str(config_path))

    engine = create_engine(db_config.url, future=True)

    # 1) Cria tabelas + trigger Python (ordem garantida)
    schema_nota_ri(engine, drop_all, env="test")

    # 2) Aplica infra FTS (depois da tabela existir)
    with open(config_path) as f:
        raw = yaml.safe_load(f)

    sql_path = ROOT / raw["nota_ri"]["infra"]["fts_init_sql_file"]

    if not sql_path.exists():
        raise RuntimeError(f"ini_fts.sql não encontrado: {sql_path}")

    with open(sql_path) as f:
        sql = f.read()

    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()

    with engine.connect() as conn:
        r = conn.execute(text("""
            SELECT tgname
            FROM pg_trigger
            WHERE tgrelid = 'nota_ri'::regclass
              AND NOT tgisinternal;
        """))
        assert list(r), "Trigger tg_update_items_document NÃO foi criado"

    yield engine

    engine.dispose()


@pytest.fixture()
def session_factory(engine):
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


@pytest.fixture(scope="session")
def app(engine):
    os.environ["BUSCA_ENV"] = "test"

    container = bootstrap()

    # FastAPI app real
    from busca.app.main import app as fastapi_app

    yield fastapi_app


@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)
