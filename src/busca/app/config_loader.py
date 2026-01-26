# busca/app/config_loader.py
import os
import yaml
from pathlib import Path

from busca.core.entity.domain_config import DatabaseConfig
from dotenv import load_dotenv

load_dotenv()


def load_nota_ri_db_config(path: str):
    env = os.getenv("BUSCA_ENV", "dev")

    with open(path) as f:
        raw = yaml.safe_load(f)

    db = raw["nota_ri"]["database"][env]

    return DatabaseConfig(**db), bool(db.get("drop_all", False))
