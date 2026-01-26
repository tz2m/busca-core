from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SearchField(BaseModel):
    name: str
    weight: str = "A"  # 'A', 'B', 'C', 'D' for Postgres FTS
    highlight: bool = False


class SearchConfig(BaseModel):
    table_name: str
    search_vector_field: str = "search_vector"
    fields: List[SearchField]


class EtlConfig(BaseModel):
    source_type: str  # 'sharepoint', 'filesystem', etc.
    source_config: Dict[str, Any]
    mapping_config: Dict[str, Any]


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    db_name: str

    @property
    def url(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'



class DomainConfig(BaseModel):
    domain_name: str
    database_config: DatabaseConfig
    search_config: SearchConfig
    etl_config: Optional[EtlConfig] = None


class SearchSchema(BaseModel):
    """Base schema for search results. Domains should inherit/compose this."""
    id: Any
    score: Optional[float] = None
    highlight: Optional[Dict[str, List[str]]] = None
    # Additional fields are dynamic or part of subclass
