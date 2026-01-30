from sqlalchemy import event, DDL

from busca.domains.material.repository.db.model.material_sql import MaterialSQL


def set_material_trigger():
    """Configura o trigger PostgreSQL para indexação FTS automática da tabela material."""
    
    # Define a função do trigger
    trigger_function_ddl = DDL("""
CREATE OR REPLACE FUNCTION update_material_document()
    RETURNS trigger AS
$$
BEGIN
    new."document" :=
                    setweight(to_tsvector('pt_br', coalesce(new."nm", '')), 'A') ||
                    setweight(to_tsvector('pt_br', coalesce(new."tipo", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."grupo", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."fab", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."nome_fab", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."txt", '')), 'C') ||
                    setweight(to_tsvector('pt_br', coalesce(new."tpc", '')), 'D') ||
                    setweight(to_tsvector('pt_br', coalesce(new."nm_ant", '')), 'D') ||
                    setweight(to_tsvector('pt_br', coalesce(new."npf", '')), 'D');
    RETURN new;
END;
$$ LANGUAGE plpgsql;
        """)

    # Define o trigger
    trigger_ddl = DDL("""
DROP TRIGGER IF EXISTS tg_update_material_document ON material;
CREATE TRIGGER tg_update_material_document
    BEFORE INSERT OR UPDATE
    ON "material"
    FOR EACH ROW
EXECUTE PROCEDURE update_material_document();
    """)

    # Anexa os DDLs ao evento after_create da tabela
    event.listen(MaterialSQL.__table__,
                 'after_create',
                 trigger_function_ddl.execute_if(dialect='postgresql'))
    event.listen(MaterialSQL.__table__,
                 'after_create',
                 trigger_ddl.execute_if(dialect='postgresql'))
