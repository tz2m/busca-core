from busca.core.use_case.search_use_case import SearchUseCase
from busca.domains.nota_ri.repository.db.search_nota_ri_repository_sql import (
    SearchNotaRiRepositorySql,
)
from tests.integration.seed_nota_ri import seed_nota_ri


def test_search_use_case_with_real_sql(session_factory):
    # popula dados reais (trigger cuida do tsvector)
    seed_nota_ri(session_factory)

    # repo real (infra)
    repo = SearchNotaRiRepositorySql(
        session=session_factory,
        debug=True,  # útil para ver SQL no teste
    )

    # use case real (application)
    uc = SearchUseCase(repo=repo)

    # executa busca real
    results = uc.execute("bomba")

    # asserções semânticas
    assert isinstance(results, list)
    assert len(results) == 1

    result = results[0]

    assert result.item.num_ri == "20041742"
    assert "bomba" in result.item.texto_descritivo_ri.lower()
    assert result.score > 0
    assert result.highlight is not None
