from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.contrib.postgres.lookups import Unaccent


class ImmutableUnaccent(Unaccent):
    """
    Unaccent that calls an immutable wrapper function (defined in init-user-db.sh)
    for postgres' unaccent function, which is not immutable - a different locale
    would return different results.

    The DB's locale is set in postgres/Dockerfile and this wrapper is safe to use
    if the locale won't ever change.
    """
    lookup_name = "f_unaccent"
    function = "f_unaccent"
models.CharField.register_lookup(ImmutableUnaccent)
models.TextField.register_lookup(ImmutableUnaccent)


class Item(models.Model):
    name = models.CharField(max_length=250)
    part_no = models.CharField(max_length=100, blank=True)
    desc = models.TextField(blank=True)

    search_vector = models.GeneratedField(
        db_persist=True,
        expression=(
            SearchVector("name", weight="A", config="cs") +
            SearchVector("desc", weight="B", config="cs")
        ),
        output_field=SearchVectorField(),
    )

    class Meta:
        ordering = ["id"]
        indexes = [
            GinIndex(
                OpClass(ImmutableUnaccent("name"), name="gin_trgm_ops"),
                name="name_idx",
            ),
            GinIndex(fields=["part_no"], name="part_no_idx", opclasses=["gin_trgm_ops"]),
            GinIndex(fields=["search_vector"], name="search_vector_idx"),
        ]

    def __str__(self):
        return self.name
