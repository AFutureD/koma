import logging
import traceback

from django.urls import path
from ninja import NinjaAPI

from .settings import SERVER_URL

logger = logging.getLogger(__name__)

api = NinjaAPI(servers = [{"url": SERVER_URL}])

api.add_router("/rag", "rag.routers.router")

@api.exception_handler(Exception)
def service_unavailable(request, exception: Exception):
    
    exception_stack = "".join(traceback.format_exception(exception))
    logger.error(exception_stack)
    
    return api.create_response(
        request,
        {"err_msg": exception.__str__(), "code": 500, "success": False},
        status=200,
    )

urlpatterns = [
    path("api/", api.urls),
]
