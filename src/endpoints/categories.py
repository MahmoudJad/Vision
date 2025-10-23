from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.get("/")
async def list_categories():
    """List categories - to be implemented"""
    return {"message": "Categories endpoint - coming soon"}