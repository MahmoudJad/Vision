from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ProductModelBase(BaseModel):
    """Base schema for ProductModel"""
    code: str = Field(..., description="Unique code for the product model", example="IPHONE_16")
    family_variant_id: Optional[UUID] = Field(None, description="ID of the family variant this product belongs to")
    parent_id: Optional[UUID] = Field(None, description="ID of the parent product model for hierarchical structure")
    category_ids: Optional[List[UUID]] = Field(default=[], description="List of category IDs this product belongs to")


class ProductModelCreate(ProductModelBase):
    """Schema for creating a new ProductModel"""
    title: str = Field(..., description="Title of the product model", example="iPhone 16")
    sku: Optional[str] = Field(None, description="Stock Keeping Unit for the product model", example="SKU12345")


class ProductModelUpdate(BaseModel):
    """Schema for updating an existing ProductModel"""
    code: Optional[str] = Field(None, description="Unique code for the product model")
    title: Optional[str] = Field(None, description="Title of the product model")
    family_variant_id: Optional[UUID] = Field(None, description="ID of the family variant")
    parent_id: Optional[UUID] = Field(None, description="ID of the parent product model")
    category_ids: Optional[List[UUID]] = Field(None, description="List of category IDs")


class ProductModelResponse(ProductModelBase):
    """Schema for ProductModel response"""
    id: UUID = Field(..., description="Unique identifier for the product model")
    title: str = Field(..., description="Title of the product model")
    created_at: datetime = Field(..., description="Timestamp when the product model was created")
    updated_at: datetime = Field(..., description="Timestamp when the product model was last updated")

    class Config:
        from_attributes = True


class ProductModelListResponse(BaseModel):
    """Schema for listing ProductModels"""
    items: List[ProductModelResponse]
    total: int
    page: int
    size: int
    pages: int