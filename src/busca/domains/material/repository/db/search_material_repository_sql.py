import re
from typing import List

from sqlalchemy import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from busca.app.dto.search_result_dto import SearchResultDTO
from busca.core.repository.search_repository import SearchRepository
from busca.domains.material.repository.db.model.material_sql import MaterialSQL


class SearchMaterialRepositorySql(SearchRepository):
    """Repositório de busca FTS para materiais usando PostgreSQL."""

    def __init__(self, session, debug: bool = False):
        self.session_factory = session
        self.debug = debug

    # -------------------------
    # Normalização de input
    # -------------------------
    @staticmethod
    def _adjust_input_text(text: str) -> str:
        """Normaliza o texto de entrada para melhorar a busca."""
        # Remove caracteres especiais extras e normaliza espaços
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    # -------------------------
    # Busca FTS com ranking + highlight
    # -------------------------
    def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        highlight: bool = True,
    ) -> List[SearchResultDTO]:
        """
        Realiza busca full-text em materiais.
        
        Args:
            query: Texto de busca
            limit: Número máximo de resultados
            offset: Offset para paginação
            highlight: Se deve incluir highlight dos termos
            
        Returns:
            Lista de SearchResultDTO com materiais encontrados
        """

        if not query.strip():
            return []

        query = self._adjust_input_text(query)

        with self.session_factory() as session:  # type: Session

            ts_query = func.websearch_to_tsquery("pt_br", query)

            rank = func.ts_rank(MaterialSQL.document, ts_query).label("rank")

            # Usa o campo tpc (descrição técnica completa) para highlight
            highlight_col = func.ts_headline(
                "pt_br",
                func.coalesce(MaterialSQL.tpc, MaterialSQL.txt),
                ts_query,
                "MaxFragments=2, FragmentDelimiter=' ... ', MaxWords=20, MinWords=10"
            ).label("highlight")

            q = (
                session.query(
                    MaterialSQL,
                    rank,
                    highlight_col,
                )
                .filter(MaterialSQL.document.op("@@")(ts_query))
                .order_by(rank.desc())
                .limit(limit)
                .offset(offset)
            )

            if self.debug:
                compiled = q.statement.compile(
                    dialect=postgresql.dialect()
                )
                print(str(compiled))

            rows = q.all()

            results: list[SearchResultDTO] = []

            for row, rank_value, highlight_value in rows:
                entity = row.to_entity()

                results.append(
                    SearchResultDTO(
                        item=entity,
                        score=float(rank_value*100),
                        highlight=highlight_value,
                    )
                )

            return results
