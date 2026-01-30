from busca.core.use_case.count_use_case import CountUseCase


class MaterialCountUseCase(CountUseCase):
    """Use case para contagem de materiais."""

    def __init__(self, repo):
        self.repo = repo

    def execute(self) -> int:
        """
        Retorna o número total de materiais cadastrados.
        
        Returns:
            Número total de materiais
        """
        return self.repo.count()
