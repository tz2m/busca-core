# busca/app/config_loader.py
import os
import yaml
from pathlib import Path

from busca.core.entity.domain_config import DatabaseConfig
from dotenv import load_dotenv

load_dotenv()


def load_nota_ri_db_config(conr):
    env = os.getenv("BUSCA_ENV", "dev")

    with open(path) as f:
        raw = yaml.safe_load(f)

    db = raw["nota_ri"]["database"][env]

    return DatabaseConfig(**db), bool(db.get("drop_all", False))


def load_material_db_config(path: str):
    """Carrega configuração de banco de dados para o domínio material."""
    env = os.getenv("BUSCA_ENV", "dev")

    with open(path) as f:
        raw = yaml.safe_load(f)

    db = raw["material"]["database"][env]

    return DatabaseConfig(**db), bool(db.get("drop_all", False))
