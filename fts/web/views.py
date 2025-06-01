from django.views.generic import ListView
from django.db.models.functions import Greatest
from django.db.models import Q
from django.contrib.postgres.search import (
    SearchQuery,
    # SearchRank,
    TrigramWordSimilarity,
    TrigramStrictWordSimilarity,
)

from .models import Item, ImmutableUnaccent


class ItemList(ListView):
    model = Item
    context_object_name = "items"
    template_name = "web/base.html"


class ItemSearchResults(ItemList):
    def get_queryset(self):
        qs = self.request.GET.get("q", "").strip()
        # No need to specify config="cs" - it's the default
        query = SearchQuery(qs, search_type="websearch")
        # Combine full-text search with similarity
        return (
            Item.objects
                .annotate(
                    # rank=SearchRank("search_vector", query, normalization=Value(32)),
                    name_similarity=TrigramStrictWordSimilarity(qs, ImmutableUnaccent('name')),
                    part_no_similarity=TrigramWordSimilarity(qs, 'part_no'),
                    similarity=Greatest(
                        # 'rank',
                        'name_similarity',
                        'part_no_similarity',
                    )
                )
                .filter(
                    Q(search_vector=query) |
                    Q(name__f_unaccent__trigram_strict_word_similar=qs) |
                    Q(part_no__trigram_word_similar=qs)
                    # Q(rank__gte=0.3) |
                    # Q(similarity__gte=0.3)
                )
                .order_by('-similarity')
        )
