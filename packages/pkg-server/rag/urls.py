from django.urls import path
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("memories/list", views.index, name="list_memories"),
    path("memories/sync", views.sync_memories, name="sync_memories"),
    path("neurons/search", views.search_neurons, name="search neurons"),
]