
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class FamilyBase(BaseModel):
    """Base schema for Family"""
    code: str = Field(..., description="Unique code for the family", example="clothing")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales", example={"en_US": "Clothing", "fr_FR": "Vêtements"})
    attributes: Optional[List[UUID]] = Field(default=[], description="List of attribute IDs associated with the family")


class FamilyCreate(FamilyBase):
    """Schema for creating a new Family"""
    code: str = Field(..., description="Unique code for the family", example="clothing")
    attributes: List[UUID] = Field(..., description="List of attribute IDs associated with the family")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales", example={"en_US": "Clothing", "fr_FR": "Vêtements"})

class FamilyUpdate(BaseModel):
    """Schema for updating an existing Family"""
    code: Optional[str] = Field(None, description="Unique code for the family")
    labels: Optional[Dict[str, str]] = Field(None, description="Labels in different locales")
    attributes: Optional[List[UUID]] = Field(None, description="List of attribute IDs associated with the family")

class FamilyResponse(FamilyBase):
    """Schema for Family response"""
    id: UUID = Field(..., description="Unique identifier for the family")
    created_at: datetime = Field(..., description="Timestamp when the family was created")
    updated_at: datetime = Field(..., description="Timestamp when the family was last updated")

    class Config:
        from_attributes = True


class FamilyListResponse(BaseModel):
    """Schema for listing Attributes"""
    items: List[FamilyResponse]
    total: int
    page: int
    size: int
    pages: int