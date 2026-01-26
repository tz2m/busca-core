from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base

from busca.domains.nota_ri.core.nota_ri import NotaRi

BaseNotaRi = declarative_base()


class NotaRiSQL(BaseNotaRi):
    __tablename__ = 'nota_ri'

    num_ri = Column(String, primary_key=True)
    ordem = Column(String)
    equipamento = Column(String)
    tag_campo = Column(String)
    local_instalacao = Column(String)
    data_max_ri = Column(String)
    desc_componente = Column(Text)
    desc_problema = Column(Text)
    texto_descritivo_ri = Column(Text)
    last_modified = Column(DateTime, nullable=False)
    document = Column(TSVECTOR)

    @classmethod
    def create_from_entity(cls, entity: NotaRi) -> 'NotaRiSQL':
        return cls(
            num_ri=entity.num_ri,
            ordem=entity.ordem,
            equipamento=entity.equipamento,
            tag_campo=entity.tag_campo,
            local_instalacao=entity.local_instalacao,
            data_max_ri=entity.data_max_ri,
            desc_componente=entity.desc_componente,
            desc_problema=entity.desc_problema,
            texto_descritivo_ri=entity.texto_descritivo_ri,
        )
    
    def to_entity(self) -> NotaRi:
        return NotaRi(
            num_ri=self.num_ri,
            ordem=self.ordem,
            equipamento=self.equipamento,
            tag_campo=self.tag_campo,
            local_instalacao=self.local_instalacao,
            data_max_ri=self.data_max_ri,
            desc_componente=self.desc_componente,
            desc_problema=self.desc_problema,
            texto_descritivo_ri=self.texto_descritivo_ri
        )