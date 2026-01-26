from busca.core.use_case.count_use_case import CountUseCase
from busca.domains.nota_ri.repository.db.nota_ri_repository_sql import NotaRIRepositorySql


class NotaRICountUseCase(CountUseCase):
    def __init__(self, repo: NotaRIRepositorySql):
        self.repo = repo

    def execute(self):
        return self.repo.size()