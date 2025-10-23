from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/families", tags=["Families"])

@router.get("/")
async def list_families():
    """List families - to be implemented"""
    return {"message": "Families endpoint - coming soon"}