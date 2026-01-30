# Vision PIM - Seed Data Quick Reference

## Overview
This document provides a quick reference for the seed data included in Vision PIM.

## Predefined UUIDs

### Attributes
| Code | ID | Type | Backend Type | Description |
|------|-----|------|--------------|-------------|
| `name` | `550e8400-e29b-41d4-a716-446655440001` | text | string | Product name (localizable) |
| `description` | `550e8400-e29b-41d4-a716-446655440002` | textarea | string | Product description (localizable, scopable) |
| `color` | `550e8400-e29b-41d4-a716-446655440003` | simple_select | option | Color attribute |
| `size` | `550e8400-e29b-41d4-a716-446655440004` | simple_select | option | Size attribute |
| `price` | `550e8400-e29b-41d4-a716-446655440005` | price | float | Price (scopable) |
| `weight` | `550e8400-e29b-41d4-a716-446655440006` | measurement | float | Weight in kg |
| `brand` | `550e8400-e29b-41d4-a716-446655440007` | text | string | Brand name |
| `material` | `550e8400-e29b-41d4-a716-446655440008` | multi_select | options | Material composition |

### Attribute Options - Color
| Code | ID | Labels |
|------|-----|--------|
| `red` | `660e8400-e29b-41d4-a716-446655440001` | en_US: Red, ar_EG: أحمر |
| `blue` | `660e8400-e29b-41d4-a716-446655440002` | en_US: Blue, ar_EG: أزرق |
| `black` | `660e8400-e29b-41d4-a716-446655440003` | en_US: Black, ar_EG: أسود |
| `white` | `660e8400-e29b-41d4-a716-446655440004` | en_US: White, ar_EG: أبيض |

### Attribute Options - Size
| Code | ID | Labels |
|------|-----|--------|
| `xs` | `660e8400-e29b-41d4-a716-446655440005` | en_US: XS, ar_EG: صغير جداً |
| `s` | `660e8400-e29b-41d4-a716-446655440006` | en_US: S, ar_EG: صغير |
| `m` | `660e8400-e29b-41d4-a716-446655440007` | en_US: M, ar_EG: متوسط |
| `l` | `660e8400-e29b-41d4-a716-446655440008` | en_US: L, ar_EG: كبير |
| `xl` | `660e8400-e29b-41d4-a716-446655440009` | en_US: XL, ar_EG: كبير جداً |

### Attribute Options - Material
| Code | ID | Labels |
|------|-----|--------|
| `cotton` | `660e8400-e29b-41d4-a716-446655440010` | en_US: Cotton, ar_EG: قطن |
| `polyester` | `660e8400-e29b-41d4-a716-446655440011` | en_US: Polyester, ar_EG: بوليستر |
| `silk` | `660e8400-e29b-41d4-a716-446655440012` | en_US: Silk, ar_EG: حرير |

### Families
| Code | ID | Description |
|------|-----|-------------|
| `clothing` | `770e8400-e29b-41d4-a716-446655440001` | Apparel products with variation attributes |
| `electronics` | `770e8400-e29b-41d4-a716-446655440002` | Electronic devices |

### Family Variants
| Code | ID | Family | Axes | Level |
|------|-----|--------|------|-------|
| `clothing_color_size` | `880e8400-e29b-41d4-a716-446655440001` | clothing | color, size | 2 |
| `electronics_simple` | `880e8400-e29b-41d4-a716-446655440002` | electronics | none | 1 |

### Categories
| Name | ID | Parent |
|------|-----|--------|
| `Apparel` | `990e8400-e29b-41d4-a716-446655440001` | - |
| `Men's Clothing` | `990e8400-e29b-41d4-a716-446655440002` | Apparel |
| `Women's Clothing` | `990e8400-e29b-41d4-a716-446655440003` | Apparel |
| `Electronics` | `990e8400-e29b-41d4-a716-446655440004` | - |

### Product Models
| Code | ID | SKU | Title | Family Variant | Categories |
|------|-----|-----|-------|----------------|------------|
| `classic_tshirt` | `aa0e8400-e29b-41d4-a716-446655440001` | PM-TSHIRT-001 | Classic T-Shirt | clothing_color_size | Men's Clothing |
| `summer_dress` | `aa0e8400-e29b-41d4-a716-446655440002` | PM-DRESS-001 | Summer Dress | clothing_color_size | Women's Clothing |

### Products
| SKU | ID | Product Model | Color | Size | Price |
|-----|-----|---------------|-------|------|-------|
| `TSHIRT-RED-M` | `bb0e8400-e29b-41d4-a716-446655440001` | classic_tshirt | Red | M | $29.99 |
| `TSHIRT-RED-L` | `bb0e8400-e29b-41d4-a716-446655440002` | classic_tshirt | Red | L | $29.99 |
| `TSHIRT-BLUE-M` | `bb0e8400-e29b-41d4-a716-446655440003` | classic_tshirt | Blue | M | $29.99 |
| `DRESS-BLACK-S` | `bb0e8400-e29b-41d4-a716-446655440004` | summer_dress | Black | S | $59.99 |
| `DRESS-BLACK-M` | `bb0e8400-e29b-41d4-a716-446655440005` | summer_dress | Black | M | $59.99 |

## Example API Requests

### Get All Attributes
```bash
curl http://localhost:8000/attributes/
```

### Get Specific Product Model
```bash
curl http://localhost:8000/products/aa0e8400-e29b-41d4-a716-446655440001
```

### Get Products by Family Variant
```bash
curl "http://localhost:8000/products/?family_variant_id=880e8400-e29b-41d4-a716-446655440001"
```

### Get Category with Children
```bash
curl http://localhost:8000/categories/990e8400-e29b-41d4-a716-446655440001/children
```

## Data Model Relationships

```
Product Values (entity_type: product_model)
  └─> Product Model: Classic T-Shirt
      ├─> Attributes:
      │   ├─> name (en_US): "Classic T-Shirt"
      │   ├─> name (ar_EG): "تيشيرت كلاسيكي"
      │   ├─> description (ecommerce, en_US): "A comfortable classic t-shirt..."
      │   └─> brand: "Generic Brand"
      │
      └─> Products:
          ├─> TSHIRT-RED-M
          │   └─> Attributes:
          │       ├─> color: Red (660e8400-e29b-41d4-a716-446655440001)
          │       ├─> size: M (660e8400-e29b-41d4-a716-446655440007)
          │       └─> price (ecommerce): 29.99
          │
          ├─> TSHIRT-RED-L
          │   └─> Attributes:
          │       ├─> color: Red
          │       ├─> size: L
          │       └─> price: 29.99
          │
          └─> TSHIRT-BLUE-M
              └─> Attributes:
                  ├─> color: Blue
                  ├─> size: M
                  └─> price: 29.99
```

## Testing the Seed Data

### 1. Verify Attributes
```bash
docker-compose exec vision python -c "
from src.database import AsyncSessionLocal
from src.model.attributes import Attribute
from sqlalchemy import select
import asyncio

async def check():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Attribute))
        attrs = result.scalars().all()
        print(f'Found {len(attrs)} attributes')
        for attr in attrs:
            print(f'  - {attr.code}: {attr.type.value}')

asyncio.run(check())
"
```

### 2. Verify Products
```bash
docker-compose exec vision python -c "
from src.database import AsyncSessionLocal
from src.model.product import Product
from sqlalchemy import select
import asyncio

async def check():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Product))
        products = result.scalars().all()
        print(f'Found {len(products)} products')
        for p in products:
            print(f'  - {p.sku}')

asyncio.run(check())
"
```

## Customization Guide

### Adding a New Attribute
1. Add to `attributes.json` with unique UUID
2. If it's a select type, add options to `attribute_options.json`
3. Add to appropriate family's `attribute_ids` in `families.json`
4. Reseed: `docker-compose exec vision python seed_database.py --force`

### Adding a New Product Variant
1. Add to `products.json` with unique SKU and UUID
2. Link to existing `product_model_id`
3. Add product values to `product_values.json` with `entity_type: "product"`
4. Specify variation axis values (color, size, etc.)
5. Reseed: `docker-compose exec vision python seed_database.py --force`

### Adding Localization
Add entries to `product_values.json` with different `locale` values:
```json
{
  "entity_type": "product_model",
  "entity_id": "aa0e8400-e29b-41d4-a716-446655440001",
  "attribute_id": "550e8400-e29b-41d4-a716-446655440001",
  "scope": null,
  "locale": "fr_FR",
  "value": "T-Shirt Classique"
}
```

### Adding Multi-Channel Pricing
Add entries with different `scope` values:
```json
{
  "entity_type": "product",
  "entity_id": "bb0e8400-e29b-41d4-a716-446655440001",
  "attribute_id": "550e8400-e29b-41d4-a716-446655440005",
  "scope": "wholesale",
  "locale": null,
  "value": 19.99
}
```
