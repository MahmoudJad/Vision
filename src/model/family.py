from sqlalchemy import Column, String, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

import uuid
from ..database import Base

class Family(Base):
    __tablename__ = "families"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    attribute_ids = Column(ARRAY(PG_UUID(as_uuid=True)))
    labels = Column(ARRAY(String), nullable=True)  # e.g., {"en_US": "Clothing", "fr_FR": "Vêtements"}