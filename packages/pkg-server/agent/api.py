from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/memories", "rag.views.memories_router")
api.add_router("/neurons", "rag.views.neurons_router")

@api.exception_handler(Exception)
def service_unavailable(request, exception: Exception):
    return api.create_response(
        request,
        {"err_msg": exception.__repr__(), "code": 500, "success": False},
        status=200,
    )
