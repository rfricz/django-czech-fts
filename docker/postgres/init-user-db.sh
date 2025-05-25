#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-"EOSQL"
    CREATE TEXT SEARCH DICTIONARY cspell (template=ispell, dictfile=czech, afffile=czech, stopwords=czech);
    CREATE TEXT SEARCH CONFIGURATION cs (copy=english);
    ALTER TEXT SEARCH CONFIGURATION cs ALTER MAPPING FOR word, asciiword WITH cspell, simple;

    CREATE EXTENSION btree_gin;
    CREATE EXTENSION pg_trgm;
    CREATE EXTENSION unaccent;

    CREATE OR REPLACE FUNCTION f_unaccent(text)
        RETURNS text
        LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
    $func$
        SELECT public.unaccent('public.unaccent', $1)
    $func$;
EOSQL
