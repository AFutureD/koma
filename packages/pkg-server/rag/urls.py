from django.urls import path

from .views import memory, neuron

urlpatterns = [
    path("memories/list", memory.list_memories, name="list_memories"),
    path("memories/sync", memory.sync_memories, name="sync_memories"),
    path("neurons/search", neuron.search_neurons, name="search neurons"),
]