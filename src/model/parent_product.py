
from sqlalchemy import Column, String, ForeignKey, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base



class ProductModel(Base):
    __tablename__ = "product_models"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    family_variant_id = Column(UUID(as_uuid=True), nullable=True)
    parent_id = Column(UUID(as_uuid=True), nullable=True)
    category_ids = Column(ARRAY(UUID(as_uuid=True)))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)