from typing import Optional
from pydantic import BaseModel, Field
import datetime


class Material(BaseModel):
    """Entidade de domínio representando um material corporativo."""

    nm: str = Field(description="Número do material")
    txt: str = Field(description="Descrição do material")
    nm_ant: Optional[str] = Field(None, description="Número anterior do material")
    umb: Optional[str] = Field(None, description="Unidade de medida base")
    tipo: Optional[str] = Field(None, description="Tipo do material")
    grupo: Optional[str] = Field(None, description="Grupo do material")
    status: Optional[str] = Field(None, description="Status do material")
    elim: Optional[str] = Field(None, description="Material eliminado (Sim/Não)")
    npf: Optional[str] = Field(None, description="Nota de processo de fabricação")
    fab: Optional[str] = Field(None, description="Código do fabricante")
    nome_fab: Optional[str] = Field(None, description="Nome do fabricante")
    tpc: Optional[str] = Field(None, description="Descrição técnica completa")
    last_modified: Optional[datetime.datetime] = Field(None, description="Data da última modificação")

    class Config:
        populate_by_name = True
