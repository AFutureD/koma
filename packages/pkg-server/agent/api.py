from ninja import NinjaAPI

api = NinjaAPI(servers = [{"url": "https://studio.afuture.me"}])

api.add_router("/rag", "rag.routers.router")


@api.exception_handler(Exception)
def service_unavailable(request, exception: Exception):
    return api.create_response(
        request,
        {"err_msg": exception.__repr__(), "code": 500, "success": False},
        status=200,
    )
