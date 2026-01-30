from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from busca.core.repository.data_repository import DataRepository
from busca.domains.material.core.material import Material
from busca.domains.material.repository.db.model.material_sql import MaterialSQL


class MaterialRepositorySql(DataRepository):
    """Repositório PostgreSQL para persistência de materiais."""

    def __init__(self, session):
        self.session_factory = session

    def save(self, material: Material) -> Material:
        """
        Salva ou atualiza um material no banco.
        
        Args:
            material: Entidade Material a ser salva
            
        Returns:
            Material salvo com last_modified atualizado
        """
        with self.session_factory() as session:  # type: Session
            material_sql = MaterialSQL.create_from_entity(material)
            material_sql.last_modified = datetime.now()
            
            session.merge(material_sql)
            session.commit()
            
            return material_sql.to_entity()

    def save_all(self, items: List[Material]) -> int:
        """
        Salva múltiplos materiais em batch.
        
        Args:
            items: Lista de materiais a serem salvos
            
        Returns:
            Número de materiais salvos
        """
        with self.session_factory() as session:  # type: Session
            now = datetime.now()
            
            for material in items:
                material_sql = MaterialSQL.create_from_entity(material)
                material_sql.last_modified = now
                session.merge(material_sql)
            
            session.commit()
            
            return len(items)

    def count(self) -> int:
        """
        Retorna o número total de materiais.
        
        Returns:
            Contagem de materiais
        """
        with self.session_factory() as session:  # type: Session
            return session.query(MaterialSQL).count()

    def find_by_id(self, material_id: int) -> Material | None:
        """
        Busca um material por ID.
        
        Args:
            material_id: ID do material
            
        Returns:
            Material encontrado ou None
        """
        with self.session_factory() as session:  # type: Session
            material_sql = session.query(MaterialSQL).filter(
                MaterialSQL.id == material_id
            ).first()
            
            return material_sql.to_entity() if material_sql else None
    def get_current_state(self) -> List[Material]:
        """Retorna todos os materiais do banco."""
        with self.session_factory() as session:  # type: Session
            rows = session.query(MaterialSQL).all()
            return [row.to_entity() for row in rows]

    def extract(self, current_state: List[Material]) -> List[Material]:
        """Extrai apenas materiais que ainda não existem no banco."""
        with self.session_factory() as session:  # type: Session
            existing_nms = {
                m_nm for (m_nm,) in session.query(MaterialSQL.nm).all()
            }
        
        return [m for m in current_state if m.nm not in existing_nms]

    def size(self) -> int:
        """Alias para count()."""
        return self.count()
