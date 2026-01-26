from typing import Optional
from pydantic import BaseModel, Field
import datetime


class NotaRi(BaseModel):
    num_ri: str = Field(alias="Núm. da RI")
    ordem: Optional[str] = Field(None, alias="Ordem")
    equipamento: Optional[str] = Field(None, alias="Equipam.")
    tag_campo: Optional[str] = Field(None, alias="TAG (Campo)")
    local_instalacao: Optional[str] = Field(None, alias="Local Instalação")
    data_max_ri: Optional[str] = Field(None, alias="Data Máx. RI")
    desc_componente: Optional[str] = Field(None, alias="Desc. Componente")
    desc_problema: Optional[str] = Field(None, alias="Desc. Problema")
    texto_descritivo_ri: Optional[str] = Field(None, alias="Texto descritivo da RI")
    last_modified: Optional[datetime.datetime] = Field(None)

    class Config:
        populate_by_name = True
