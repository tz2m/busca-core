import pandas as pd
from typing import List, Any
from pathlib import Path
import datetime

from busca.core.repository.data_repository import DataRepository
from busca.domains.nota_ri.core.nota_ri import NotaRi


class NotaRIRepositoryCSV(DataRepository):

    def save_all(self, items: List[Any]) -> int:
        raise NotImplementedError("Método save_all não implementado para CSV.")

    def __init__(self, file: str | Path):
        self.file = Path(file)
        if not self.file.exists() or not self.file.is_file():
            raise ValueError(f"O caminho {self.file.absolute()} não é um arquivo válido.")

    # -----------------------------
    # Leitura do CSV → Lista[NotaRi]
    # -----------------------------
    def get_current_state(self) -> List[NotaRi]:
        if not self.file.exists():
            return []

        df = pd.read_csv(
            self.file,
            sep=";",
            dtype=str,
            keep_default_na=False,
        )

        # Remove coluna índice "#" se existir
        if df.columns[0].startswith("#"):
            df = df.iloc[:, 1:]

        notas: List[NotaRi] = []

        for _, row in df.iterrows():
            data = row.to_dict()

            # Normaliza last_modified
            if "last_modified" in data and data["last_modified"]:
                data["last_modified"] = datetime.datetime.fromisoformat(
                    data["last_modified"]
                )

            nota = NotaRi(**data)
            notas.append(nota)

        return notas

    # -----------------------------
    # Extrai apenas novos itens
    # -----------------------------
    def extract(self, current_state: List[NotaRi]) -> List[NotaRi]:
        csv_state = self.get_current_state()

        current_ids = {item.num_ri for item in current_state}
        new_items = [item for item in csv_state if item.num_ri not in current_ids]

        return new_items

    # -----------------------------
    # Persiste um item no CSV
    # -----------------------------
    def save(self, item: NotaRi):
        data = item.dict(by_alias=True)

        # Normaliza datetime para string
        if data.get("last_modified"):
            data["last_modified"] = data["last_modified"].isoformat()

        df_new = pd.DataFrame([data])

        # Arquivo ainda não existe
        if not self.file.exists():
            df_new.to_csv(
                self.file,
                sep=";",
                index=False,
            )
            return

        # Arquivo já existe → append
        df = pd.read_csv(
            self.file,
            sep=";",
            dtype=str,
            keep_default_na=False,
        )

        df = pd.concat([df, df_new], ignore_index=True)

        df.to_csv(
            self.file,
            sep=";",
            index=False,
        )

    # -----------------------------
    # Retorna tamanho do CSV
    # -----------------------------
    def size(self) -> int:
        if not self.file.exists():
            return 0

        df = pd.read_csv(
            self.file,
            sep=";",
            dtype=str,
            keep_default_na=False,
        )

        return len(df)
