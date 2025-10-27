from fastapi import APIRouter
from src.endpoints.products import router as products_router
from src.endpoints.categories import router as categories_router
from src.endpoints.attributes import router as attributes_router
from src.endpoints.attribute_options import router as attribute_options_router
from src.endpoints.families import router as families_router

router = APIRouter()

# Include all endpoint routers
router.include_router(
    products_router,
    prefix="/api/v1/product-models",
    tags=["Product Models"]
    )

router.include_router(
    attributes_router,
    prefix="/api/v1/attributes", 
    tags=["Attributes"]
    )

router.include_router(
    attribute_options_router,
    prefix="/api/v1/attributes", 
    tags=["Attribute Options"]
    )

router.include_router(
    families_router,
    prefix="/api/v1/families",
    tags=["Families"]
)

router.include_router(
    categories_router,
    prefix="/api/v1/categories",
    tags=["Categories"]
)