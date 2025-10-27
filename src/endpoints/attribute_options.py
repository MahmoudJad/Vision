from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from ..database import get_db
from ..model.attributes import Attribute, AttributeOption
from ..schemas.attribute import (
    AttributeOptionCreate,
    AttributeOptionResponse,
    AttributeOptionBase
)
from ..enums.enum import AttributeType

router = APIRouter()


@router.post("/{attribute_id}/options", response_model=AttributeOptionResponse, status_code=201)
async def create_attribute_option(
    attribute_id: UUID = Path(..., description="ID of the attribute to add option to"),
    option_data: AttributeOptionCreate = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new option to an existing select attribute.
    
    Only works with simple_select and multi_select attribute types.
    """
    try:
        # Check if attribute exists and is a select type
        attribute_query = select(Attribute).where(Attribute.id == attribute_id)
        attribute_result = await db.execute(attribute_query)
        attribute = attribute_result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID '{attribute_id}' not found"
            )
        
        if attribute.type not in [AttributeType.SIMPLE_SELECT, AttributeType.MULTI_SELECT]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot add options to attribute type '{attribute.type}'. Only simple_select and multi_select attributes support options."
            )
        
        # Check if option code already exists for this attribute
        existing_option_query = select(AttributeOption).where(
            AttributeOption.attribute_id == attribute_id,
            AttributeOption.code == option_data.code
        )
        existing_option_result = await db.execute(existing_option_query)
        existing_option = existing_option_result.scalar_one_or_none()
        
        if existing_option:
            raise HTTPException(
                status_code=400,
                detail=f"Option with code '{option_data.code}' already exists for this attribute"
            )
        
        # Create new option
        option = AttributeOption(
            attribute_id=attribute_id,
            code=option_data.code,
            labels=option_data.labels,
            sort_order=option_data.sort_order
        )
        
        db.add(option)
        await db.commit()
        await db.refresh(option)
        
        return option
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to create attribute option: {str(e)}")


@router.get("/{attribute_id}/options", response_model=List[AttributeOptionResponse])
async def list_attribute_options(
    attribute_id: UUID = Path(..., description="ID of the attribute to list options for"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all options for a specific attribute.
    """
    try:
        # Check if attribute exists
        attribute_query = select(Attribute).where(Attribute.id == attribute_id)
        attribute_result = await db.execute(attribute_query)
        attribute = attribute_result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID '{attribute_id}' not found"
            )
        
        # Get all options for this attribute
        options_query = select(AttributeOption).where(
            AttributeOption.attribute_id == attribute_id
        ).order_by(AttributeOption.sort_order, AttributeOption.code)
        
        options_result = await db.execute(options_query)
        options = options_result.scalars().all()
        
        return options
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to list attribute options: {str(e)}")


@router.put("/{attribute_id}/options/reorder", response_model=List[AttributeOptionResponse])
async def reorder_attribute_options(
    attribute_id: UUID = Path(..., description="ID of the attribute"),
    option_order: List[UUID] = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    Reorder attribute options by providing a list of option IDs in the desired order.
    
    The sort_order field will be updated automatically based on the position in the list.
    """
    try:
        # Check if attribute exists
        attribute_query = select(Attribute).where(Attribute.id == attribute_id)
        attribute_result = await db.execute(attribute_query)
        attribute = attribute_result.scalar_one_or_none()
        
        if not attribute:
            raise HTTPException(
                status_code=404,
                detail=f"Attribute with ID '{attribute_id}' not found"
            )
        
        # Get all options for this attribute
        options_query = select(AttributeOption).where(
            AttributeOption.attribute_id == attribute_id
        )
        
        options_result = await db.execute(options_query)
        options = options_result.scalars().all()
        option_dict = {option.id: option for option in options}
        
        # Validate that all provided option IDs belong to this attribute
        for option_id in option_order:
            if option_id not in option_dict:
                raise HTTPException(
                    status_code=400,
                    detail=f"Option ID '{option_id}' does not belong to attribute '{attribute_id}'"
                )
        
        # Validate that all options are included in the reorder list
        if len(option_order) != len(options):
            raise HTTPException(
                status_code=400,
                detail=f"Reorder list must include all {len(options)} options for this attribute"
            )
        
        # Update sort_order for each option
        for index, option_id in enumerate(option_order):
            option = option_dict[option_id]
            option.sort_order = str(index + 1)
        
        await db.commit()
        
        # Return the reordered options
        reordered_options_query = select(AttributeOption).where(
            AttributeOption.attribute_id == attribute_id
        ).order_by(AttributeOption.sort_order)
        
        reordered_result = await db.execute(reordered_options_query)
        reordered_options = reordered_result.scalars().all()
        
        return reordered_options
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to reorder attribute options: {str(e)}")


@router.get("/{attribute_id}/options/{option_id}", response_model=AttributeOptionResponse)
async def get_attribute_option(
    attribute_id: UUID = Path(..., description="ID of the attribute"),
    option_id: UUID = Path(..., description="ID of the option to retrieve"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific attribute option by ID.
    """
    try:
        # Get the option and verify it belongs to the specified attribute
        option_query = select(AttributeOption).where(
            AttributeOption.id == option_id,
            AttributeOption.attribute_id == attribute_id
        )
        
        option_result = await db.execute(option_query)
        option = option_result.scalar_one_or_none()
        
        if not option:
            raise HTTPException(
                status_code=404,
                detail=f"Option with ID '{option_id}' not found for attribute '{attribute_id}'"
            )
        
        return option
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to get attribute option: {str(e)}")


@router.put("/{attribute_id}/options/{option_id}", response_model=AttributeOptionResponse)
async def update_attribute_option(
    attribute_id: UUID = Path(..., description="ID of the attribute"),
    option_id: UUID = Path(..., description="ID of the option to update"),
    option_data: AttributeOptionBase = ...,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing attribute option.
    """
    try:
        # Get the option and verify it belongs to the specified attribute
        option_query = select(AttributeOption).where(
            AttributeOption.id == option_id,
            AttributeOption.attribute_id == attribute_id
        )
        
        option_result = await db.execute(option_query)
        option = option_result.scalar_one_or_none()
        
        if not option:
            raise HTTPException(
                status_code=404,
                detail=f"Option with ID '{option_id}' not found for attribute '{attribute_id}'"
            )
        
        # Check if the new code conflicts with existing options (if code is being changed)
        if option_data.code != option.code:
            existing_code_query = select(AttributeOption).where(
                AttributeOption.attribute_id == attribute_id,
                AttributeOption.code == option_data.code,
                AttributeOption.id != option_id
            )
            existing_code_result = await db.execute(existing_code_query)
            existing_code_option = existing_code_result.scalar_one_or_none()
            
            if existing_code_option:
                raise HTTPException(
                    status_code=400,
                    detail=f"Option with code '{option_data.code}' already exists for this attribute"
                )
        
        # Update the option
        option.code = option_data.code
        option.labels = option_data.labels
        option.sort_order = option_data.sort_order
        
        await db.commit()
        await db.refresh(option)
        
        return option
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to update attribute option: {str(e)}")


@router.delete("/{attribute_id}/options/{option_id}", status_code=204)
async def delete_attribute_option(
    attribute_id: UUID = Path(..., description="ID of the attribute"),
    option_id: UUID = Path(..., description="ID of the option to delete"),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific attribute option.
    
    Warning: This will also remove any product values that reference this option.
    """
    try:
        # Verify the option exists and belongs to the specified attribute
        option_query = select(AttributeOption).where(
            AttributeOption.id == option_id,
            AttributeOption.attribute_id == attribute_id
        )
        
        option_result = await db.execute(option_query)
        option = option_result.scalar_one_or_none()
        
        if not option:
            raise HTTPException(
                status_code=404,
                detail=f"Option with ID '{option_id}' not found for attribute '{attribute_id}'"
            )
        
        # Delete the option
        delete_query = delete(AttributeOption).where(
            AttributeOption.id == option_id,
            AttributeOption.attribute_id == attribute_id
        )
        
        await db.execute(delete_query)
        await db.commit()
        
        # Return 204 No Content (successful deletion)
        return None
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to delete attribute option: {str(e)}")