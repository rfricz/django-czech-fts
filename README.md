# Django PostgreSQL Full-text & Similarity Search in Czech (v češtině)

A working example of full-text search and trigram similarity search in Czech language using PostgreSQL database and Django.

Fulltextové a přibližné vyhledávání v češtině v PostgreSQL databázi s použitím Django.

## How It Works

The setup is based on the [17-bookworm](https://hub.docker.com/_/postgres) Postgres docker image:

1. In a custom Postgres [Dockerfile](docker/postgres/Dockerfile) (see [Locale Customization](https://github.com/docker-library/docs/blob/master/postgres/README.md#locale-customization)):
   * The `cs_CZ` locale is defined and `LANG` environment variable is set to `cs_CZ.UTF-8`; error messages are kept in `en_US`
   * `czech.{affix,dict,stop}` files are extracted to Postgres’ `tsearch_data` directory (see [postgres.cz](https://postgres.cz/wiki/Instalace_PostgreSQL#Instalace_Fulltextu))
   * [init-user-db.sh](docker/postgres/init-user-db.sh) script (see [Database Configuration](https://github.com/docker-library/docs/blob/master/postgres/README.md#database-configuration)) that will be run by Postgres during the initial startup is copied in
2. In [init-user-db.sh](docker/postgres/init-user-db.sh):
   * Text search configuration `cs` is created and set as the `default_text_search_config`
   * The extensions for GIN index, trigram similarity and unaccent are activated
   * An immutable wrapper function for Postgres’ `unaccent` function is created
3. The `Item` model in [models.py](fts/web/models.py):
   * Creates a generated [`SearchVectorField`](https://docs.djangoproject.com/en/5.2/ref/contrib/postgres/search/#searchvectorfield) that uses the `cs` text search configuration
   * Includes a GIN index for the search vector field, a simple trigram index and a trigram index created by applying the unaccent operation (see [Creating Indexes](https://www.postgresql.org/docs/17/textsearch-tables.html#TEXTSEARCH-TABLES-INDEX))
4. The `ItemSearchResults` view in [views.py](fts/web/views.py) combines full-text search with similarity

## How To Run It

A simplified deployment config with Caddy and Debian-based Python and Postgres images is provided. Use Docker Compose to start everything up:
```bash
docker compose up -d
```
And then go to https://fts.localhost/ in your browser. The DB is prepopulated with a few pangrams in Czech and 500 rows of random lorem ipsum. Use the search field or the search URL like [https://fts.localhost/search?q=kůň](https://fts.localhost/search?q=k%C5%AF%C5%88).

By leveraging the specialized GIN indexes included in the model, the search query plan can avoid costly sequential scans in the DB most of the time, depending on the data and the searched text. Use the SQL explain function of the included django-debug-toolbar, e.g. searching for 'kůň' results in Bitmap Index Scan:
```
Sort  (cost=95.86..95.86 rows=1 width=546) (actual time=0.175..0.176 rows=1 loops=1)
  Sort Key: (GREATEST(strict_word_similarity('kůň'::text, f_unaccent((name)::text)), word_similarity('kůň'::text, (part_no)::text))) DESC
  Sort Method: quicksort  Memory: 25kB
  ->  Bitmap Heap Scan on web_item  (cost=90.82..95.85 rows=1 width=546) (actual time=0.160..0.161 rows=1 loops=1)
        Recheck Cond: ((search_vector @@ websearch_to_tsquery('kůň'::text)) OR (f_unaccent((name)::text) %>> 'kun'::text) OR ((part_no)::text %> 'kůň'::text))
        Heap Blocks: exact=1
        ->  BitmapOr  (cost=90.82..90.82 rows=1 width=0) (actual time=0.051..0.052 rows=0 loops=1)
              ->  Bitmap Index Scan on search_vector_idx  (cost=0.00..13.07 rows=1 width=0) (actual time=0.022..0.022 rows=1 loops=1)
                    Index Cond: (search_vector @@ websearch_to_tsquery('kůň'::text))
              ->  Bitmap Index Scan on name_idx  (cost=0.00..38.88 rows=1 width=0) (actual time=0.019..0.019 rows=0 loops=1)
                    Index Cond: (f_unaccent((name)::text) %>> 'kun'::text)
              ->  Bitmap Index Scan on part_no_idx  (cost=0.00..38.88 rows=1 width=0) (actual time=0.009..0.009 rows=0 loops=1)
                    Index Cond: ((part_no)::text %> 'kůň'::text)
Planning Time: 235.480 ms
Execution Time: 0.240 ms
```
