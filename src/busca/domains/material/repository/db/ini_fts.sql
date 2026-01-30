-- Script SQL de inicialização FTS para o domínio Material
-- Este script reutiliza a configuração pt_br já criada pelo domínio nota_ri

-- Criando a função material_tsquery para facilitar buscas
CREATE OR REPLACE FUNCTION material_tsquery(word text)
RETURNS tsquery AS $$
BEGIN
    RETURN websearch_to_tsquery('pt_br', trim(word));
END;
$$ LANGUAGE plpgsql;
