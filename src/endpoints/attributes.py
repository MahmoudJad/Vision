from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
import math

from ..database import get_db
from ..model.attributes import Attribute, AttributeOption
from ..schemas.attribute import (
    AttributeCreate,
    AttributeUpdate,
    AttributeResponse,
    AttributeListResponse
)
from ..enums.enum import AttributeType, BackendType

router = APIRouter()


@router.post("/", response_model=AttributeResponse, status_code=201)
async def create_attribute(
    attribute_data: AttributeCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new attribute.
    
    Attributes define the structure and type of data that can be stored for products.
    For example: color (simple_select), weight (number), description (text).
    """
    try:
        # Check if code already exists
        existing_query = select(Attribute).where(Attribute.code == attribute_data.code)
        existing_result = await db.execute(existing_query)
        existing_attribute = existing_result.scalar_one_or_none()
        
        if existing_attribute:
            raise HTTPException(
                status_code=400,
                detail=f"Attribute with code '{attribute_data.code}' already exists"
            )
        
        # Create new attribute
        attribute = Attribute(
            code=attribute_data.code,
            type=attribute_data.type,
            backend_type=attribute_data.backend_type,
            is_localizable=attribute_data.is_localizable,
            is_scopable=attribute_data.is_scopable,
            group_code=attribute_data.group_code,
            labels=attribute_data.labels,
            config=attribute_data.config
        )
        
        db.add(attribute)
        await db.commit()
        await db.refresh(attribute)
        
        # Add options if provided (for select types)
        if attribute_data.options and attribute_data.type in [AttributeType.SIMPLE_SELECT, AttributeType.MULTI_SELECT]:
            for option_data in attribute_data.options:
                option = AttributeOption(
                    attribute_id=attribute.id,
                    code=option_data.code,
                    labels=option_data.labels,
                    sort_order=option_data.sort_order
                )
                db.add(option)
            
            await db.commit()
            await db.refresh(attribute)
        
        # Load the attribute with options
        query = select(Attribute).options(selectinload(Attribute.options)).where(Attribute.id == attribute.id)
        result = await db.execute(query)
        attribute = result.scalar_one()
        
        return attribute
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to create attribute: {str(e)}")


@router.get("/", response_model=AttributeListResponse)
async def list_attributes(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: str = Query(None, description="Search by code or label"),
    type: Optional[AttributeType] = Query(None, description="Filter by attribute type"),
    backend_type: Optional[BackendType] = Query(None, description="Filter by backend type"),
    group_code: str = Query(None, description="Filter by group code"),
    is_localizable: Optional[bool] = Query(None, description="Filter by localizable flag"),
    is_scopable: Optional[bool] = Query(None, description="Filter by scopable flag"),
    db: AsyncSession = Depends(get_db)
):
    """
    List attributes with pagination and filtering.
    """
    try:
        # Build base query
        query = select(Attribute).options(selectinload(Attribute.options))
        count_query = select(func.count(Attribute.id))
        
        # Apply filters
        if search:
            search_filter = Attribute.code.ilike(f"%{search}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        if type:
            query = query.where(Attribute.type == type)
            count_query = count_query.where(Attribute.type == type)
        
        if backend_type:
            query = query.where(Attribute.backend_type == backend_type)
            count_query = count_query.where(Attribute.backend_type == backend_type)
        
        if group_code:
            query = query.where(Attribute.group_code == group_code)
            count_query = count_query.where(Attribute.group_code == group_code)
        
        if is_localizable is not None:
            query = query.where(Attribute.is_localizable == is_localizable)
            count_query = count_query.where(Attribute.is_localizable == is_localizable)
        
        if is_scopable is not None:
            query = query.where(Attribute.is_scopable == is_scopable)
            count_query = count_query.where(Attribute.is_scopable == is_scopable)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(Attribute.created_at.desc())
        
        # Execute query
        result = await db.execute(query)
        attributes = result.scalars().all()
        
        # Calculate pagination info
        pages = math.ceil(total / size) if total > 0 else 0
        
        return AttributeListResponse(
            items=attributes,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list attributes: {str(e)}")


@router.get("/{attribute_id}", response_model=AttributeResponse)
async def get_attribute(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific attribute by ID.
    """
    try:
        query = select(Attribute).options(selectinload(Attribute.options)).where(Attribute.id == attribute_id)
        result = await db.execute(query)
        attribute = result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID {attribute_id} not found"
            )
        
        return attribute
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get attribute: {str(e)}")


@router.put("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(
    attribute_id: UUID,
    attribute_data: AttributeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing attribute.
    """
    try:
        # Get existing attribute
        query = select(Attribute).options(selectinload(Attribute.options)).where(Attribute.id == attribute_id)
        result = await db.execute(query)
        attribute = result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID {attribute_id} not found"
            )
        
        # Check if new code already exists (if code is being updated)
        if attribute_data.code and attribute_data.code != attribute.code:
            existing_query = select(Attribute).where(Attribute.code == attribute_data.code)
            existing_result = await db.execute(existing_query)
            existing_attribute = existing_result.scalar_one_or_none()
            
            if existing_attribute:
                raise HTTPException(
                    status_code=400,
                    detail=f"Attribute with code '{attribute_data.code}' already exists"
                )
        
        # Update fields
        update_data = attribute_data.dict(exclude_unset=True, exclude={'options'})
        for field, value in update_data.items():
            setattr(attribute, field, value)
        
        # Handle options update if provided
        if attribute_data.options is not None:
            # Remove existing options
            for option in attribute.options:
                await db.delete(option)
            
            # Add new options
            for option_data in attribute_data.options:
                option = AttributeOption(
                    attribute_id=attribute.id,
                    code=option_data.code,
                    labels=option_data.labels,
                    sort_order=option_data.sort_order
                )
                db.add(option)
        
        await db.commit()
        await db.refresh(attribute)
        
        return attribute
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update attribute: {str(e)}")


@router.delete("/{attribute_id}")
async def delete_attribute(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an attribute.
    
    Note: This will also delete all associated attribute options and product values.
    """
    try:
        # Get existing attribute
        query = select(Attribute).where(Attribute.id == attribute_id)
        result = await db.execute(query)
        attribute = result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID {attribute_id} not found"
            )
        
        await db.delete(attribute)
        await db.commit()
        
        return {"message": f"Attribute {attribute_id} deleted successfully"}
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete attribute: {str(e)}")


@router.get("/types/attribute-types")
async def get_attribute_types():
    """
    Get all available attribute types.
    """
    return {
        "attribute_types": [
            {"value": type.value, "label": type.value.replace("_", " ").title()}
            for type in AttributeType
        ]
    }


@router.get("/types/backend-types")
async def get_backend_types():
    """
    Get all available backend types.
    """
    return {
        "backend_types": [
            {"value": type.value, "label": type.value.replace("_", " ").title()}
            for type in BackendType
        ]
    }