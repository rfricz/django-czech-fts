# Django PostgreSQL Full-text & Similarity Search in Czech (v češtině)

A working example of full-text search and trigram similarity search in Czech language using PostgreSQL database and Django.

---

Fulltextové a přibližné vyhledávání v češtině v PostgreSQL databázi s použitím Django.

---

A simplified deployment config with Caddy and Debian-based Python and Postgres images is provided. Use Docker Compose to start everything up:
```bash
docker compose up -d
```
And then go to https://fts.localhost/ in your browser. The DB is prepopulated with a few pangrams in Czech and 500 rows of random lorem ipsum. Use the search field or the search URL like [https://fts.localhost/search?q=kůň](https://fts.localhost/search?q=k%C5%AF%C5%88).

By leveraging the specialized GIN indexes included in the model, the search query plan can avoid costly sequential scans in the DB most of the time, depending on the data and the searched text. Use the SQL explain function of the included django-debug-toolbar, e.g. searching for 'kůň' results in Bitmap Index Scan:
```
Sort  (cost=95.36..95.36 rows=1 width=566) (actual time=0.122..0.123 rows=1 loops=1)
  Sort Key: (GREATEST(strict_word_similarity('kůň'::text, f_unaccent((name)::text)), word_similarity('kůň'::text, (part_no)::text))) DESC
  Sort Method: quicksort  Memory: 25kB
  ->  Bitmap Heap Scan on web_item  (cost=90.57..95.35 rows=1 width=566) (actual time=0.107..0.108 rows=1 loops=1)
        Recheck Cond: ((search_vector @@ '''kůň'''::tsquery) OR (f_unaccent((name)::text) %>> 'kun'::text) OR ((part_no)::text %> 'kůň'::text))
        Heap Blocks: exact=1
        ->  BitmapOr  (cost=90.57..90.57 rows=1 width=0) (actual time=0.039..0.039 rows=0 loops=1)
              ->  Bitmap Index Scan on search_vector_idx  (cost=0.00..12.82 rows=1 width=0) (actual time=0.010..0.010 rows=1 loops=1)
                    Index Cond: (search_vector @@ '''kůň'''::tsquery)
              ->  Bitmap Index Scan on name_idx  (cost=0.00..38.88 rows=1 width=0) (actual time=0.015..0.015 rows=0 loops=1)
                    Index Cond: (f_unaccent((name)::text) %>> 'kun'::text)
              ->  Bitmap Index Scan on part_no_idx  (cost=0.00..38.88 rows=1 width=0) (actual time=0.013..0.013 rows=0 loops=1)
                    Index Cond: ((part_no)::text %> 'kůň'::text)
Planning Time: 222.990 ms
Execution Time: 0.182 ms
```
