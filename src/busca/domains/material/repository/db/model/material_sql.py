from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base

from busca.domains.material.core.material import Material

BaseMaterial = declarative_base()


class MaterialSQL(BaseMaterial):
    """Modelo SQLAlchemy para a tabela material no PostgreSQL."""
    
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    nm = Column(String, nullable=False)
    txt = Column(Text, nullable=False)
    nm_ant = Column(String)
    umb = Column(String)
    tipo = Column(String)
    grupo = Column(String)
    status = Column(String)
    elim = Column(String)
    npf = Column(String)
    fab = Column(String)
    nome_fab = Column(String)
    tpc = Column(Text)
    last_modified = Column(DateTime, nullable=False)
    document = Column(TSVECTOR)

    @classmethod
    def create_from_entity(cls, entity: Material) -> 'MaterialSQL':
        """Cria uma instância MaterialSQL a partir de uma entidade Material."""
        return cls(
            nm=entity.nm,
            txt=entity.txt,
            nm_ant=entity.nm_ant,
            umb=entity.umb,
            tipo=entity.tipo,
            grupo=entity.grupo,
            status=entity.status,
            elim=entity.elim,
            npf=entity.npf,
            fab=entity.fab,
            nome_fab=entity.nome_fab,
            tpc=entity.tpc,
        )
    
    def to_entity(self) -> Material:
        """Converte MaterialSQL para entidade Material."""
        return Material(
            nm=self.nm,
            txt=self.txt,
            nm_ant=self.nm_ant,
            umb=self.umb,
            tipo=self.tipo,
            grupo=self.grupo,
            status=self.status,
            elim=self.elim,
            npf=self.npf,
            fab=self.fab,
            nome_fab=self.nome_fab,
            tpc=self.tpc,
            last_modified=self.last_modified,
        )
