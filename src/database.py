from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config import settings

# Create async engine with proper configuration
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create base class for models
Base = declarative_base()

# Import all models to register them with Base
def import_models():
    """Import all models to ensure they are registered with SQLAlchemy"""
    from src.model import (
        Attribute, AttributeOption, ProductValue, 
        Product, ProductModel, Family, FamilyVariant
    )

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()