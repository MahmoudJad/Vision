from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/attributes", tags=["Attributes"])

@router.get("/")
async def list_attributes():
    """List attributes - to be implemented"""
    return {"message": "Attributes endpoint - coming soon"}