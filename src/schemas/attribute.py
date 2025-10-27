from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from ..enums.enum import AttributeType, BackendType


class AttributeOptionBase(BaseModel):
    """Base schema for AttributeOption"""
    code: str = Field(..., description="Unique code for the attribute option", example="red")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales", example={"en_US": "Red", "ar_EG": "أحمر"})
    sort_order: Optional[str] = Field(None, description="Sort order for display", example="1")


class AttributeOptionCreate(AttributeOptionBase):
    """Schema for creating a new AttributeOption"""
    pass


class AttributeOptionResponse(AttributeOptionBase):
    """Schema for AttributeOption response"""
    id: UUID = Field(..., description="Unique identifier for the attribute option")

    class Config:
        from_attributes = True


class AttributeBase(BaseModel):
    """Base schema for Attribute"""
    code: str = Field(..., description="Unique code for the attribute", example="color")
    type: AttributeType = Field(..., description="Type of the attribute")
    backend_type: BackendType = Field(..., description="Backend storage type")
    is_localizable: bool = Field(default=False, description="Whether the attribute is localizable")
    is_scopable: bool = Field(default=False, description="Whether the attribute is scopable")
    group_code: Optional[str] = Field(None, description="Group code for organizing attributes", example="general")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales", example={"en_US": "Color", "ar_EG": "اللون"})
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration", example={"unit": "cm", "min": 0, "max": 100})


class AttributeCreate(AttributeBase):
    """Schema for creating a new Attribute"""
    options: Optional[List[AttributeOptionCreate]] = Field(default=[], description="Attribute options for select types")


class AttributeUpdate(BaseModel):
    """Schema for updating an existing Attribute"""
    code: Optional[str] = Field(None, description="Unique code for the attribute")
    type: Optional[AttributeType] = Field(None, description="Type of the attribute")
    backend_type: Optional[BackendType] = Field(None, description="Backend storage type")
    is_localizable: Optional[bool] = Field(None, description="Whether the attribute is localizable")
    is_scopable: Optional[bool] = Field(None, description="Whether the attribute is scopable")
    group_code: Optional[str] = Field(None, description="Group code for organizing attributes")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales")
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration")
    options: Optional[List[AttributeOptionCreate]] = Field(None, description="Attribute options for select types")


class AttributeResponse(AttributeBase):
    """Schema for Attribute response"""
    id: UUID = Field(..., description="Unique identifier for the attribute")
    created_at: datetime = Field(..., description="Timestamp when the attribute was created")
    updated_at: datetime = Field(..., description="Timestamp when the attribute was last updated")
    options: List[AttributeOptionResponse] = Field(default=[], description="Attribute options")

    class Config:
        from_attributes = True


class AttributeListResponse(BaseModel):
    """Schema for listing Attributes"""
    items: List[AttributeResponse]
    total: int
    page: int
    size: int
    pages: int