import sqlite3
from typing import List
from pathlib import Path

from busca.core.repository.data_repository import DataRepository
from busca.domains.material.core.material import Material


class MaterialRepositorySqlite(DataRepository):
    """Repositório para leitura de materiais do banco SQLite original."""

    def __init__(self, file: str):
        self.file = Path(file)
        
        if not self.file.exists():
            raise FileNotFoundError(f"SQLite database not found: {self.file}")

    def find_all(self) -> List[Material]:
        """
        Lê todos os materiais do banco SQLite.
        
        Returns:
            Lista de entidades Material
        """
        conn = sqlite3.connect(self.file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, nm, txt, nm_ant, umb, tipo, grupo, 
                status, elim, npf, fab, nome_fab, tpc
            FROM nms
            ORDER BY id
        """)
        
        materials = []
        for row in cursor.fetchall():
            material = Material(
                id=row['id'],
                nm=row['nm'] or '',
                txt=row['txt'] or '',
                nm_ant=row['nm_ant'],
                umb=row['umb'],
                tipo=row['tipo'],
                grupo=row['grupo'],
                status=row['status'],
                elim=row['elim'],
                npf=row['npf'],
                fab=row['fab'],
                nome_fab=row['nome_fab'],
                tpc=row['tpc'],
            )
            materials.append(material)
        
        conn.close()
        
        return materials

    def count(self) -> int:
        """
        Retorna o número total de materiais no SQLite.
        
        Returns:
            Contagem de materiais
        """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM nms")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return count
    def get_current_state(self) -> List[Material]:
        """Alias para find_all() para cumprir interface DataRepository."""
        return self.find_all()

    def extract(self, current_state: List[Material]) -> List[Material]:
        """Não implementado para o repositório original."""
        raise NotImplementedError("Extract não disponível para SQLite original.")

    def save(self, item: Material):
        """Não implementado para o repositório original."""
        raise NotImplementedError("Save não disponível para SQLite original.")


    def save_all(self, item: Material):
        """Não implementado para o repositório original."""
        raise NotImplementedError("Save não disponível para SQLite original.")

    def size(self) -> int:
        """Alias para count() para cumprir interface DataRepository."""
        return self.count()
