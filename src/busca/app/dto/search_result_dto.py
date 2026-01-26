from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SearchResultDTO(BaseModel, Generic[T]):
    """
    DTO genérico para encapsular o resultado da busca FTS
    sem poluir a entidade de domínio.
    """

    item: T
    score: float
    highlight: Optional[str] = None

    # Metadados opcionais (futuro)
    domain: Optional[str] = None
    source: Optional[str] = None
    link: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            T: lambda v: v.dict(by_alias=False)
        }
