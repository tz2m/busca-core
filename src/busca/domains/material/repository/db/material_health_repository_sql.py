from sqlalchemy import Engine, inspect, text

from busca.core.repository.health_repository import HealthRepository


class MaterialHealthRepository(HealthRepository):
    """Repositório de health check para o domínio material."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def check(self) -> dict:
        """
        Verifica a saúde do domínio material.
        
        Valida:
        - Conectividade com o banco
        - Existência da tabela material
        - Existência do trigger FTS
        
        Returns:
            Dicionário com status de saúde
        """
        try:
            with self.engine.connect() as connection:
                inspector = inspect(connection)
                
                # Verifica se a tabela existe
                tables = inspector.get_table_names()
                table_exists = 'material' in tables
                
                if not table_exists:
                    return {
                        "status": "down",
                        "domain": "material",
                        "database": "ok",
                        "table": "missing",
                        "fts_trigger": "unknown"
                    }
                
                # Verifica se o trigger existe
                trigger_check = text("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM pg_trigger 
                        WHERE tgname = 'tg_update_material_document'
                    );
                """)
                
                result = connection.execute(trigger_check)
                trigger_exists = result.scalar()
                
                return {
                    "status": "ok" if trigger_exists else "degraded",
                    "domain": "material",
                    "database": "ok",
                    "table": "ok",
                    "fts_trigger": "ok" if trigger_exists else "missing"
                }
                
        except Exception as e:
            return {
                "status": "down",
                "domain": "material",
                "database": "error",
                "error": str(e)
            }
