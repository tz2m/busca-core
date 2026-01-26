from typing import Any, List, Iterator
import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from busca.core.repository.data_repository import DataRepository
from busca.domains.nota_ri.core.nota_ri import NotaRi
from busca.domains.nota_ri.repository.db.model.nota_ri_sql import NotaRiSQL


class NotaRIRepositorySql(DataRepository):

    def __init__(self, session):
        """
        session: sessionmaker injetado pelo Container
        """
        self.session_factory = session

    # --------------------------------
    # Retorna estado atual (tudo)
    # --------------------------------
    def get_current_state(self) -> List[NotaRi]:
        with self.session_factory() as session:  # type: Session
            rows = session.query(NotaRiSQL).all()
            return [row.to_entity() for row in rows]

    # --------------------------------
    # Extrai apenas novos itens (delta)
    # --------------------------------
    def extract(self, current_state: List[Any]) -> Iterator[Any]:
        """
        current_state: List[NotaRi]
        Retorna apenas itens ainda não persistidos no banco
        """
        with self.session_factory() as session:  # type: Session
            existing_ids = {
                num_ri
                for (num_ri,) in session.query(NotaRiSQL.num_ri).all()
            }

        for item in current_state:
            if item.num_ri not in existing_ids:
                yield item

    # --------------------------------
    # Persiste item (UPSERT sem SQL bruto)
    # --------------------------------
    def save(self, item: NotaRi):
        with self.session_factory() as session:  # type: Session
            existing = session.get(NotaRiSQL, item.num_ri)

            if existing:
                # Atualiza campos
                existing.ordem = item.ordem
                existing.equipamento = item.equipamento
                existing.tag_campo = item.tag_campo
                existing.local_instalacao = item.local_instalacao
                existing.data_max_ri = item.data_max_ri
                existing.desc_componente = item.desc_componente
                existing.desc_problema = item.desc_problema
                existing.texto_descritivo_ri = item.texto_descritivo_ri
                existing.last_modified = item.last_modified or datetime.datetime.now()
            else:
                # Insere novo
                row = NotaRiSQL.create_from_entity(item)
                row.last_modified = item.last_modified or datetime.datetime.now()
                session.add(row)

            session.commit()

    # --------------------------------
    # Retorna quantidade de registros
    # --------------------------------
    def size(self) -> int:
        with self.session_factory() as session:
            return session.query(func.count(NotaRiSQL.num_ri)).scalar()
