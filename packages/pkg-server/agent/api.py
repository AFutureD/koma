from ninja import NinjaAPI
import traceback

api = NinjaAPI(servers = [{"url": "https://studio.afuture.me"}])

api.add_router("/rag", "rag.routers.router")

import logging

logger = logging.getLogger(__name__)

@api.exception_handler(Exception)
def service_unavailable(request, exception: Exception):
    
    exception_stack = "".join(traceback.format_exception(exception))
    logger.error(exception_stack)
    
    return api.create_response(
        request,
        {"err_msg": exception.__str__(), "code": 500, "success": False},
        status=200,
    )
