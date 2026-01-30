-- Copia o script SQL de inicialização para criar o dicionário e a configuração no DockerFile
-- COPY init_fts.sql /docker-entrypoint-initdb.d/

DROP TEXT SEARCH DICTIONARY IF EXISTS dict_simple_ptbr CASCADE;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE TEXT SEARCH DICTIONARY public.dict_simple_ptbr (
    TEMPLATE = pg_catalog.simple,
    STOPWORDS = portuguese,
    Accept = false
    );
DROP TEXT SEARCH DICTIONARY IF EXISTS dict_ispell_ptbr CASCADE;
CREATE TEXT SEARCH DICTIONARY dict_ispell_ptbr (
    TEMPLATE = ispell,
    DictFile = hunspell_pt_br,
    AffFile = hunspell_pt_br,
    StopWords = portuguese
    );
DROP TEXT SEARCH DICTIONARY IF EXISTS dict_snowball_ptbr CASCADE;
CREATE TEXT SEARCH DICTIONARY dict_snowball_ptbr (
    TEMPLATE = snowball,
    Language = portuguese,
    StopWords = portuguese
    );
DROP TEXT SEARCH CONFIGURATION IF EXISTS pt_br CASCADE;
CREATE TEXT SEARCH CONFIGURATION pt_br (COPY =pg_catalog.portuguese);
ALTER TEXT SEARCH CONFIGURATION pt_br ALTER MAPPING FOR asciiword, asciihword, hword_asciipart, word, hword, hword_part
    WITH unaccent, portuguese_stem, dict_simple_ptbr, dict_ispell_ptbr, dict_snowball_ptbr;
