from sqlalchemy import Column, String, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from ..database import Base


class FamilyVariant(Base):
    __tablename__ = "family_variants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"))
    code = Column(String, unique=True, nullable=False)
    level = Column(String)
    axes = Column(ARRAY(UUID(as_uuid=True)))  # variation attributes
    attributes = Column(ARRAY(UUID(as_uuid=True)))