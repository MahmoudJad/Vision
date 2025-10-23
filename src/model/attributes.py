from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base


class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)  # e.g., "text", "simple_select", "number"
    backend_type = Column(String, nullable=False)  # e.g., "string", "float"
    is_localizable = Column(Boolean, default=False)
    is_scopable = Column(Boolean, default=False)
    group_code = Column(String, nullable=True)
    labels = Column(JSON)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    options = relationship("AttributeOption", back_populates="attribute", cascade="all, delete-orphan")


class AttributeOption(Base):
    __tablename__ = "attribute_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey("attributes.id"))
    code = Column(String, nullable=False)
    labels = Column(JSON)
    sort_order = Column(Integer, default=0)

    attribute = relationship("Attribute", back_populates="options")
