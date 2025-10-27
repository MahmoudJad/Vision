from enum import Enum as PyEnum

class AttributeType(PyEnum):
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SIMPLE_SELECT = "simple_select"
    MULTI_SELECT = "multi_select"
    DATE = "date"
    PRICE = "price"
    IMAGE = "image"


class BackendType(PyEnum):
    STRING = "string"
    FLOAT = "float"
    BOOLEAN = "boolean"
    OPTION = "option"
    OPTIONS = "options"
    DATE = "date"
    JSON = "json"


class EntityType(PyEnum):
    PRODUCT = "product"
    PRODUCT_MODEL = "product_model"