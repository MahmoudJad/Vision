
from sqlalchemy import (
    Column, String, ForeignKey, JSON, Enum, DateTime, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from ..enums.enum import EntityType
import uuid
from ..database import Base  # assuming you have a shared Base declarative instance

class ProductValue(Base):
    __tablename__ = "product_values"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(Enum(EntityType), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    attribute_id = Column(UUID(as_uuid=True), ForeignKey("attributes.id", ondelete="CASCADE"), nullable=False)
    scope = Column(String, nullable=True)   # e.g. "ecommerce", "mobile"
    locale = Column(String, nullable=True)  # e.g. "en_US", "ar_EG"
    value = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attribute = relationship("Attribute", back_populates="values")

    __table_args__ = (
        Index("uq_entity_attr_scope_locale", "entity_type", "entity_id", "attribute_id", "scope", "locale", unique=True),
    )