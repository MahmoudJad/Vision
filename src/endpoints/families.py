from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_families():
    """List families - to be implemented"""
    return {"message": "Families endpoint - coming soon"}