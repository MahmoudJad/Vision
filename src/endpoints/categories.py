from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID
import math

from ..database import get_db
from ..model.category import Category
from ..schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListResponse
)

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new category.
    
    Categories are used to organize products into hierarchical groups.
    They can have parent categories to create a tree structure.
    """
    try:
        # Check if name already exists
        existing_query = select(Category).where(Category.name == category_data.name)
        existing_result = await db.execute(existing_query)
        existing_category = existing_result.scalar_one_or_none()
        
        if existing_category:
            raise HTTPException(
                status_code=400,
                detail=f"Category with name '{category_data.name}' already exists"
            )
        
        # Validate parent_id if provided
        if category_data.parent_id:
            parent_query = select(Category).where(Category.id == category_data.parent_id)
            parent_result = await db.execute(parent_query)
            parent_category = parent_result.scalar_one_or_none()
            
            if not parent_category:
                raise HTTPException(
                    status_code=404,
                    detail=f"Parent category with ID {category_data.parent_id} not found"
                )
        
        # Create new category
        category = Category(
            name=category_data.name,
            description=category_data.description,
            parent_id=category_data.parent_id
        )
        
        db.add(category)
        await db.commit()
        await db.refresh(category)
        
        return category
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")


@router.get("/", response_model=CategoryListResponse)
async def list_categories(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    parent_id: Optional[UUID] = Query(None, description="Filter by parent category ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    List categories with pagination and filtering.
    """
    try:
        # Build base query
        query = select(Category)
        count_query = select(func.count(Category.id))
        
        # Apply filters
        if search:
            search_filter = (
                Category.name.ilike(f"%{search}%") | 
                Category.description.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        if parent_id is not None:
            query = query.where(Category.parent_id == parent_id)
            count_query = count_query.where(Category.parent_id == parent_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(Category.name)
        
        # Execute query
        result = await db.execute(query)
        categories = result.scalars().all()
        
        # Calculate pagination info
        pages = math.ceil(total / size) if total > 0 else 0
        
        return CategoryListResponse(
            items=categories,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list categories: {str(e)}")


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific category by ID.
    """
    try:
        query = select(Category).where(Category.id == category_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {category_id} not found"
            )
        
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category: {str(e)}")


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing category.
    """
    try:
        # Get existing category
        query = select(Category).where(Category.id == category_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Check if new name already exists (if name is being updated)
        if category_data.name and category_data.name != category.name:
            existing_query = select(Category).where(Category.name == category_data.name)
            existing_result = await db.execute(existing_query)
            existing_category = existing_result.scalar_one_or_none()
            
            if existing_category:
                raise HTTPException(
                    status_code=400,
                    detail=f"Category with name '{category_data.name}' already exists"
                )
        
        # Validate parent_id if being updated
        if category_data.parent_id is not None:
            # Prevent setting category as its own parent
            if category_data.parent_id == category_id:
                raise HTTPException(
                    status_code=400,
                    detail="A category cannot be its own parent"
                )
            
            # Check if parent exists
            parent_query = select(Category).where(Category.id == category_data.parent_id)
            parent_result = await db.execute(parent_query)
            parent_category = parent_result.scalar_one_or_none()
            
            if not parent_category:
                raise HTTPException(
                    status_code=404,
                    detail=f"Parent category with ID {category_data.parent_id} not found"
                )
        
        # Update fields
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        await db.commit()
        await db.refresh(category)
        
        return category
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update category: {str(e)}")


@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a category.
    
    Note: This will fail if there are child categories. Delete or reassign children first.
    """
    try:
        # Get existing category
        query = select(Category).where(Category.id == category_id)
        result = await db.execute(query)
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Check for child categories
        children_query = select(func.count(Category.id)).where(Category.parent_id == category_id)
        children_result = await db.execute(children_query)
        children_count = children_result.scalar()
        
        if children_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete category with {children_count} child categories. Delete or reassign children first."
            )
        
        await db.delete(category)
        await db.commit()
        
        return {"message": f"Category {category_id} deleted successfully"}
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete category: {str(e)}")


@router.get("/{category_id}/children", response_model=CategoryListResponse)
async def get_category_children(
    category_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all child categories for a given parent category.
    """
    try:
        # Check if parent exists
        parent_query = select(Category).where(Category.id == category_id)
        parent_result = await db.execute(parent_query)
        parent_category = parent_result.scalar_one_or_none()
        
        if not parent_category:
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {category_id} not found"
            )
        
        # Get children
        query = select(Category).where(Category.parent_id == category_id)
        count_query = select(func.count(Category.id)).where(Category.parent_id == category_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(Category.name)
        
        # Execute query
        result = await db.execute(query)
        children = result.scalars().all()
        
        # Calculate pagination info
        pages = math.ceil(total / size) if total > 0 else 0
        
        return CategoryListResponse(
            items=children,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category children: {str(e)}")