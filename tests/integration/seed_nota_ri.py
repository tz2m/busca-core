import datetime
from sqlalchemy.orm import Session

from busca.domains.nota_ri.repository.db.model.nota_ri_sql import NotaRiSQL


def seed_nota_ri(session_factory):
    with session_factory() as session:  # type: Session
        session.query(NotaRiSQL).delete()

        rows = [
            NotaRiSQL(
                num_ri="20041742",
                ordem="52045277",
                equipamento="10289428",
                tag_campo="TQ-631402",
                local_instalacao="SUA.BNK.ARMZNT.TQ-631402",
                data_max_ri="45834",
                desc_componente="BACIA DE CONTENÇÃO-ACESSOS",
                desc_problema="PROCESSO CORROSIVO",
                texto_descritivo_ri="Problema grave de corrosão na bomba principal",
                last_modified=datetime.datetime(2025, 6, 15),
            ),
            NotaRiSQL(
                num_ri="20043998",
                ordem=None,
                equipamento=None,
                tag_campo=None,
                local_instalacao="SUA.GLP.PIER01",
                data_max_ri="42973",
                desc_componente=None,
                desc_problema=None,
                texto_descritivo_ri="Inspeção visual em válvula auxiliar",
                last_modified=datetime.datetime(2025, 6, 10),
            ),
        ]

        session.add_all(rows)
        session.commit()
