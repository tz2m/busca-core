import re
from typing import List

from sqlalchemy import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from busca.app.dto.search_result_dto import SearchResultDTO
from busca.core.repository.search_repository import SearchRepository
from busca.domains.nota_ri.repository.db.model.nota_ri_sql import NotaRiSQL


class SearchNotaRiRepositorySql(SearchRepository):

    def __init__(self, session, debug: bool = False):
        self.session_factory = session
        self.debug = debug

    # -------------------------
    # Normalização de input
    # -------------------------
    @staticmethod
    def _adjust_input_text(text: str) -> str:
        pattern = r'[A-Za-z]{2}-\d[A-Za-z]{2}-\d{1,6}'

        def replace_hyphen(match):
            part = match.group().replace('-', ' ').split(" ")
            return f"{part[0]} {part[1]} {part[2].zfill(5)}"

        return re.sub(pattern, replace_hyphen, text)

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

        if not query.strip():
            return []

        query = self._adjust_input_text(query)

        with self.session_factory() as session:  # type: Session

            ts_query = func.plainto_tsquery("portuguese", query)

            rank = func.ts_rank(NotaRiSQL.document, ts_query).label("rank")

            highlight_col = func.ts_headline(
                "portuguese",
                NotaRiSQL.texto_descritivo_ri,
                ts_query,
                "MaxFragments=2, FragmentDelimiter=' ... ', MaxWords=20, MinWords=10"
            ).label("highlight")

            q = (
                session.query(
                    NotaRiSQL,
                    rank,
                    highlight_col,
                )
                .filter(NotaRiSQL.document.op("@@")(ts_query))
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
                        score=float(rank_value),
                        highlight=highlight_value,
                    )
                )

            return results