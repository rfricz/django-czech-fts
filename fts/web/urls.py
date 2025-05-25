from django.urls import path

from .views import ItemList, ItemSearchResults

urlpatterns = [
    path("", ItemList.as_view(), name="item_list"),
    path("search", ItemSearchResults.as_view(), name="item_search_results"),
]
