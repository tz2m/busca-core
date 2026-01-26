from sqlalchemy import text

from busca.core.repository.health_repository import HealthRepository


class NotaRIHealthRepository(HealthRepository):
    def __init__(self, engine):
        self.engine = engine

    def check(self) -> dict:
        try:
            with self.engine.connect() as conn:

                # 1) Verifica conectividade básica
                conn.execute(text("SELECT 1"))

                # 2) Verifica existência do trigger FTS
                r = conn.execute(text("""
                    SELECT 1
                    FROM pg_trigger
                    WHERE tgname = 'tg_update_items_document'
                      AND NOT tgisinternal;
                """))

                trigger_ok = r.first() is not None

                if not trigger_ok:
                    return {
                        "status": "degraded",
                        "domain": "nota_ri",
                        "database": "ok",
                        "fts_trigger": "missing",
                        "detail": "Trigger tg_update_items_document não encontrado",
                    }

                # 3) Tudo OK
                return {
                    "status": "ok",
                    "domain": "nota_ri",
                    "database": "ok",
                    "fts_trigger": "ok",
                }

        except Exception as e:
            return {
                "status": "error",
                "domain": "nota_ri",
                "database": "down",
                "fts_trigger": "unknown",
                "detail": str(e),
            }
