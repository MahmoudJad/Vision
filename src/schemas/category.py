from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class CategoryBase(BaseModel):
    """Base schema for Category"""
    name: str = Field(..., description="Unique name for the category", example="Electronics")
    description: Optional[str] = Field(None, description="Description of the category", example="Electronic devices and accessories")
    parent_id: Optional[UUID] = Field(None, description="Parent category ID for nested categories")


class CategoryCreate(CategoryBase):
    """Schema for creating a new Category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating an existing Category"""
    name: Optional[str] = Field(None, description="Unique name for the category")
    description: Optional[str] = Field(None, description="Description of the category")
    parent_id: Optional[UUID] = Field(None, description="Parent category ID for nested categories")


class CategoryResponse(CategoryBase):
    """Schema for Category response"""
    id: UUID = Field(..., description="Unique identifier for the category")
    created_at: datetime = Field(..., description="Timestamp when the category was created")
    updated_at: datetime = Field(..., description="Timestamp when the category was last updated")

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for listing Categories"""
    items: List[CategoryResponse]
    total: int
    page: int
    size: int
    pages: int
