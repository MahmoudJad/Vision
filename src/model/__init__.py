# Import all models to ensure they are registered with SQLAlchemy
# Import order matters to resolve relationships properly

from .attributes import Attribute, AttributeOption
from .product_values import ProductValue
from .product import Product
from .parent_product import ProductModel
from .family import Family
from .family_variants import FamilyVariant

__all__ = [
    "Attribute",
    "AttributeOption",
    "ProductValue",
    "Product",
    "ProductModel",
    "Family",
    "FamilyVariant",
]
