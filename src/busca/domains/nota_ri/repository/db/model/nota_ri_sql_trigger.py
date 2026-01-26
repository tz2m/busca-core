from sqlalchemy import (event,
                        DDL)

from busca.domains.nota_ri.repository.db.model.nota_ri_sql import NotaRiSQL


def set_nota_ri_tigger():
    # Define the trigger function and trigger DDL statements
    trigger_function_ddl = DDL("""
CREATE OR REPLACE FUNCTION update_items_document()
    RETURNS trigger AS
$$
BEGIN
    new."document" :=
                    setweight(to_tsvector('pt_br', coalesce(new."num_ri", '')), 'A') ||
                    setweight(to_tsvector('pt_br', coalesce(new."equipamento", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."ordem", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."tag_campo", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."local_instalacao", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."data_max_ri", '')), 'B') ||
                    setweight(to_tsvector('pt_br', coalesce(new."desc_componente", '')), 'C') ||
                    setweight(to_tsvector('pt_br', coalesce(new."desc_problema", '')), 'C') ||
                    setweight(to_tsvector('pt_br', coalesce(new."texto_descritivo_ri", '')), 'D');
    RETURN new;
END;
$$ LANGUAGE plpgsql;
        """)

    trigger_ddl = DDL("""
DROP TRIGGER IF EXISTS tg_update_items_document ON nota_ri;
CREATE TRIGGER tg_update_items_document
    BEFORE INSERT OR UPDATE
    ON "nota_ri"
    FOR EACH ROW
EXECUTE PROCEDURE update_items_document();
    """)

    # Attach the DDL to an event
    event.listen(NotaRiSQL.__table__,
                 'after_create',
                 trigger_function_ddl.execute_if(dialect='postgresql'))
    event.listen(NotaRiSQL.__table__,
                 'after_create',
                 trigger_ddl.execute_if(dialect='postgresql'))
