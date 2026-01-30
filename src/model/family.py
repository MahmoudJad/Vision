from sqlalchemy import Column, String, ARRAY, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import uuid
from ..database import Base

class Family(Base):
    __tablename__ = "families"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    attribute_ids = Column(ARRAY(PG_UUID(as_uuid=True)))
    labels = Column(JSON, nullable=True)  # e.g., {"en_US": "Clothing", "ar_EG": "ملابس"}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)