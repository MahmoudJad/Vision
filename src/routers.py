from fastapi import APIRouter
from src.endpoints.products import router as products_router
from src.endpoints.categories import router as categories_router
from src.endpoints.attributes import router as attributes_router
from src.endpoints.families import router as families_router

router = APIRouter()

# Include all endpoint routers
router.include_router(products_router)
router.include_router(categories_router)
router.include_router(attributes_router)
router.include_router(families_router)