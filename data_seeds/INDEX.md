# Vision PIM - Database Seeding Documentation

Welcome to the Vision PIM database seeding documentation! This directory contains everything you need to understand and customize the seed data for the Vision PIM system.

## 📚 Documentation Files

### 📖 [README.md](README.md)
**Complete guide to database seeding**
- Overview of the seeding system
- File structure and relationships
- Usage instructions
- Customization guide
- Entity relationship diagrams

### 🔍 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Quick lookup for all seed data**
- Tables of all predefined UUIDs
- Attribute definitions
- Option mappings
- Product examples
- API request examples
- Testing commands

### 🎨 [STRUCTURE.md](STRUCTURE.md)
**Visual representation of data flow**
- ASCII diagrams showing relationships
- Data flow on creation
- Attribute value inheritance
- Multi-locale and multi-scope support
- Seeding order dependencies

## 📦 Data Files

### Core Definitions
1. **[attributes.json](attributes.json)** - 8 product attributes
2. **[attribute_options.json](attribute_options.json)** - 12 options for select attributes
3. **[families.json](families.json)** - 2 product families
4. **[family_variants.json](family_variants.json)** - 2 family variants

### Organization
5. **[categories.json](categories.json)** - 4 hierarchical categories

### Products
6. **[product_models.json](product_models.json)** - 2 product templates
7. **[products.json](products.json)** - 5 product variants
8. **[product_values.json](product_values.json)** - Attribute values for all products

## 🚀 Quick Start

### View Sample Data
```bash
# See all attributes
cat data_seeds/attributes.json | jq '.[] | {code, type, backend_type}'

# See all products
cat data_seeds/products.json | jq '.[] | {sku, product_model_id}'

# See product values for a specific product
cat data_seeds/product_values.json | jq '.[] | select(.entity_id == "bb0e8400-e29b-41d4-a716-446655440001")'
```

### Run Seeding
```bash
# Automatic (runs on docker-compose up)
docker-compose up -d

# Manual
docker-compose exec vision python seed_database.py

# Force reseed
docker-compose exec vision python seed_database.py --force

# Reset and reseed
docker-compose exec vision bash reset_and_seed.sh
```

## 🎯 Common Use Cases

### 1. Understanding the Data Model
Start with **[STRUCTURE.md](STRUCTURE.md)** to see visual diagrams of how everything connects.

### 2. Finding Specific IDs
Use **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** for quick lookups of UUIDs and codes.

### 3. Adding New Data
Follow the guides in **[README.md](README.md)** for step-by-step instructions on extending the seed data.

### 4. Testing API Endpoints
Use the example requests in **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** to test your API.

## 📊 What's Included

### Sample Product Catalog

#### Classic T-Shirt (Men's)
- **Product Model**: PM-TSHIRT-001
- **Variants**: 3 products
  - Red / M → $29.99
  - Red / L → $29.99
  - Blue / M → $29.99
- **Attributes**: Name, Description, Brand, Color, Size, Price
- **Localization**: English & Arabic names

#### Summer Dress (Women's)
- **Product Model**: PM-DRESS-001
- **Variants**: 2 products
  - Black / S → $59.99
  - Black / M → $59.99
- **Attributes**: Name, Description, Brand, Color, Size, Price
- **Localization**: English name

### Configuration Options

#### Locales
- `en_US` - English (United States)
- `ar_EG` - Arabic (Egypt)

#### Scopes (Channels)
- `ecommerce` - E-commerce website
- `mobile` - Mobile application

#### Attribute Groups
- `general` - General product info
- `variation` - Variation attributes
- `pricing` - Price-related attributes
- `physical` - Physical properties

## 🔧 Customization Examples

### Add a New Color
Edit `attribute_options.json`:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440013",
  "attribute_id": "550e8400-e29b-41d4-a716-446655440003",
  "code": "green",
  "labels": {
    "en_US": "Green",
    "ar_EG": "أخضر"
  },
  "sort_order": "5"
}
```

### Add a New Product Variant
Edit `products.json`:
```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440006",
  "sku": "TSHIRT-GREEN-M",
  "product_model_id": "aa0e8400-e29b-41d4-a716-446655440001",
  "enabled": true
}
```

Then add product values in `product_values.json`.

### Add Multi-Currency Pricing
Edit `product_values.json`:
```json
{
  "entity_type": "product",
  "entity_id": "bb0e8400-e29b-41d4-a716-446655440001",
  "attribute_id": "550e8400-e29b-41d4-a716-446655440005",
  "scope": "ecommerce_eu",
  "locale": null,
  "value": 24.99
}
```

## ⚠️ Important Notes

1. **UUIDs must be unique** - Generate new UUIDs for new records
2. **Maintain referential integrity** - Ensure IDs reference existing records
3. **Follow seeding order** - Some files depend on others
4. **Check enum values** - Attribute types and entity types must match defined enums
5. **Test after changes** - Run the seeder to verify your changes

## 🧪 Testing Your Changes

After modifying seed data:

```bash
# 1. Reset database
docker-compose exec vision bash reset_and_seed.sh

# 2. Verify data loaded correctly
docker-compose exec vision python -c "
from src.database import AsyncSessionLocal
from src.model.product import Product
from sqlalchemy import select, func
import asyncio

async def verify():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(Product.id)))
        count = result.scalar()
        print(f'✅ Found {count} products in database')

asyncio.run(verify())
"

# 3. Test API endpoints
curl http://localhost:8000/products/ | jq
curl http://localhost:8000/attributes/ | jq
curl http://localhost:8000/categories/ | jq
```

## 🆘 Troubleshooting

### Seeding Fails with Foreign Key Error
- Check that referenced IDs exist in their respective files
- Verify seeding order (attributes before families, families before variants, etc.)

### Duplicate Key Error
- Run with `--force` flag to skip duplicates
- Or reset database completely with `reset_and_seed.sh`

### Invalid UUID Format
- Ensure all UUIDs match pattern: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Generate new UUIDs with `python -c "import uuid; print(uuid.uuid4())"`

### Invalid Enum Value
- Check attribute `type` values match `AttributeType` enum
- Check attribute `backend_type` values match `BackendType` enum
- Check product value `entity_type` matches `EntityType` enum

## 📞 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review [STRUCTURE.md](STRUCTURE.md) for visual diagrams
- Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick lookups
- See the main project README for general setup instructions

---

**Happy Seeding! 🌱**
