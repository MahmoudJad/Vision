from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_categories():
    """List categories - to be implemented"""
    return {"message": "Categories endpoint - coming soon"}