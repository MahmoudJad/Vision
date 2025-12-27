from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, String

from src.schemas.family import FamilyListResponse, FamilyCreate, FamilyUpdate
from src.model.family import Family
from ..database import get_db


router = APIRouter()

@router.get("/", response_model=FamilyListResponse, summary="List all families")
async def list_families(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search by code or label"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a list of all families."""
    try:
        # build the base query
        query = select(Family).order_by(Family.code)
        count_query = select(func.count(Family.id))
        if search:
            search_pattern = f"%{search}%"
            query = query.where(
                (Family.code.ilike(search_pattern)) |
                (func.cast(Family.labels, String).ilike(search_pattern))
            )
            count_query = count_query.where(
                (Family.code.ilike(search_pattern)) |
                (func.cast(Family.labels, String).ilike(search_pattern))
            )
        # get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()
        # apply pagination
        query = query.offset((page - 1) * size).limit(size)
        result = await db.execute(query)
        families = result.scalars().all()   
        return FamilyListResponse(
            items=families,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    except Exception as e:
        print(f"Error retrieving families: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list families: {str(e)}")
    

@router.get("/{family_code}", response_model=FamilyListResponse, summary="Get family by code")
async def get_family_by_code(
    family_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a family by its unique code."""
    try:
        query = select(Family).where(Family.code == family_code)
        result = await db.execute(query)
        family = result.scalar_one_or_none()
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")
        return family
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving family {family_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get family: {str(e)}")


@router.post("/", response_model=FamilyListResponse, summary="Create a new family")
async def create_family(
    family: FamilyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new family."""
    try:
        new_family = Family(
            code=family.code,
            attribute_ids=family.attribute_ids,
            labels=family.labels
        )
        db.add(new_family)
        await db.commit()
        await db.refresh(new_family)
        return new_family
    except Exception as e:
        print(f"Error creating family: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create family: {str(e)}")

    