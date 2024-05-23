from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/memories", "rag.views.memories_router")
api.add_router("/neurons", "rag.views.neurons_router")