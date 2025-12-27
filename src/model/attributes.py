from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base
from ..enums.enum import AttributeType, BackendType

class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    type = Column(Enum(AttributeType), nullable=False)  # e.g., "text", "simple_select", "number"
    backend_type = Column(Enum(BackendType), nullable=False)  # e.g., "string", "float"
    is_localizable = Column(Boolean, default=False)
    is_scopable = Column(Boolean, default=False)
    group_code = Column(String, nullable=True)
    labels = Column(JSON, nullable=True)  # {"en_US": "Color", "ar_EG": "اللون"}
    # config: extra metadata for UI, constraints, etc.
    config = Column(JSON, nullable=True)  # {"unit": "cm", "min": 0, "max": 100}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    options = relationship("AttributeOption", back_populates="attribute", cascade="all, delete-orphan")
    # Note: ProductValue relationship commented out temporarily to avoid circular import
    values = relationship("ProductValue", back_populates="attribute", cascade="all, delete-orphan")


class AttributeOption(Base):
    __tablename__ = "attribute_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey("attributes.id", ondelete="CASCADE"))
    code = Column(String, nullable=False)
    labels = Column(JSON, nullable=True)  # {"en_US": "Red", "ar_EG": "أحمر"}
    sort_order = Column(String, nullable=True)

    attribute = relationship("Attribute", back_populates="options")
