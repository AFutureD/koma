from ninja import Router

from .views import memories_router, neurons_router

router = Router()

router.add_router("/memories", memories_router)
router.add_router("/neurons", neurons_router)