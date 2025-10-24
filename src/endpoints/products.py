from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from uuid import UUID
import math

from ..database import get_db
from ..model.parent_product import ProductModel
from ..schemas.product_model import (
    ProductModelCreate,
    ProductModelUpdate,
    ProductModelResponse,
    ProductModelListResponse
)

router = APIRouter()


@router.post("/create", response_model=ProductModelResponse, status_code=201)
async def create_product_model(
    payload: ProductModelCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new parent product (ProductModel).
    
    Parent products serve as templates containing common attributes between 
    types of specific products. For example, if you want to create product 
    variants like "iPhone 16, 128GB, Red", the parent product would contain 
    the attributes that refer to "iPhone 16".
    """
    try:
        # Check if code already exists
        existing_query = select(ProductModel).where(ProductModel.code == payload.code)
        existing_result = await db.execute(existing_query)
        existing_product = existing_result.scalar_one_or_none()
        
        if existing_product:
            raise HTTPException(
                status_code=400,
                detail=f"Product model with code '{payload.code}' already exists"
            )
        
        # Create new product model
        product_model = ProductModel(
            code=payload.code,
            title=payload.title,
            sku=payload.sku,
            family_variant_id=payload.family_variant_id,
            parent_id=payload.parent_id,
            category_ids=payload.category_ids or []
        )
        
        db.add(product_model)
        await db.commit()
        await db.refresh(product_model)
        
        return product_model
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to create product model: {str(e)}")


@router.get("/", response_model=ProductModelListResponse)
async def list_product_models(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: str = Query(None, description="Search by code"),
    family_variant_id: UUID = Query(None, description="Filter by family variant ID"),
    parent_id: UUID = Query(None, description="Filter by parent ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    List product models with pagination and filtering.
    """
    try:
        # Build base query
        query = select(ProductModel)
        count_query = select(func.count(ProductModel.id))
        
        # Apply filters
        if search:
            query = query.where(ProductModel.code.ilike(f"%{search}%"))
            count_query = count_query.where(ProductModel.code.ilike(f"%{search}%"))
        
        if family_variant_id:
            query = query.where(ProductModel.family_variant_id == family_variant_id)
            count_query = count_query.where(ProductModel.family_variant_id == family_variant_id)
        
        if parent_id:
            query = query.where(ProductModel.parent_id == parent_id)
            count_query = count_query.where(ProductModel.parent_id == parent_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(ProductModel.created_at.desc())
        
        # Execute query
        result = await db.execute(query)
        product_models = result.scalars().all()
        
        # Calculate pagination info
        pages = math.ceil(total / size) if total > 0 else 0
        
        return ProductModelListResponse(
            items=product_models,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list product models: {str(e)}")


@router.get("/{product_model_id}", response_model=ProductModelResponse)
async def get_product_model(
    product_model_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific product model by ID.
    """
    try:
        query = select(ProductModel).where(ProductModel.id == product_model_id)
        result = await db.execute(query)
        product_model = result.scalar_one_or_none()
        
        if not product_model:
            raise HTTPException(
                status_code=404,
                detail=f"Product model with ID {product_model_id} not found"
            )
        
        return product_model
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product model: {str(e)}")


@router.put("/{product_model_id}", response_model=ProductModelResponse)
async def update_product_model(
    product_model_id: UUID,
    product_model_data: ProductModelUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing product model.
    """
    try:
        # Get existing product model
        query = select(ProductModel).where(ProductModel.id == product_model_id)
        result = await db.execute(query)
        product_model = result.scalar_one_or_none()
        
        if not product_model:
            raise HTTPException(
                status_code=404,
                detail=f"Product model with ID {product_model_id} not found"
            )
        
        # Check if new code already exists (if code is being updated)
        if product_model_data.code and product_model_data.code != product_model.code:
            existing_query = select(ProductModel).where(ProductModel.code == product_model_data.code)
            existing_result = await db.execute(existing_query)
            existing_product = existing_result.scalar_one_or_none()
            
            if existing_product:
                raise HTTPException(
                    status_code=400,
                    detail=f"Product model with code '{product_model_data.code}' already exists"
                )
        
        # Update fields
        update_data = product_model_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product_model, field, value)
        
        await db.commit()
        await db.refresh(product_model)
        
        return product_model
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update product model: {str(e)}")


@router.delete("/{product_model_id}")
async def delete_product_model(
    product_model_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a product model.
    """
    try:
        # Get existing product model
        query = select(ProductModel).where(ProductModel.id == product_model_id)
        result = await db.execute(query)
        product_model = result.scalar_one_or_none()
        
        if not product_model:
            raise HTTPException(
                status_code=404,
                detail=f"Product model with ID {product_model_id} not found"
            )
        
        await db.delete(product_model)
        await db.commit()
        
        return {"message": f"Product model {product_model_id} deleted successfully"}
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete product model: {str(e)}")


@router.get("/{product_model_id}/children", response_model=ProductModelListResponse)
async def get_product_model_children(
    product_model_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all child product models for a given parent product model.
    """
    try:
        # Check if parent exists
        parent_query = select(ProductModel).where(ProductModel.id == product_model_id)
        parent_result = await db.execute(parent_query)
        parent_product = parent_result.scalar_one_or_none()
        
        if not parent_product:
            raise HTTPException(
                status_code=404,
                detail=f"Product model with ID {product_model_id} not found"
            )
        
        # Get children
        query = select(ProductModel).where(ProductModel.parent_id == product_model_id)
        count_query = select(func.count(ProductModel.id)).where(ProductModel.parent_id == product_model_id)
        
        # Get total count
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(ProductModel.created_at.desc())
        
        # Execute query
        result = await db.execute(query)
        children = result.scalars().all()
        
        # Calculate pagination info
        pages = math.ceil(total / size) if total > 0 else 0
        
        return ProductModelListResponse(
            items=children,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product model children: {str(e)}")