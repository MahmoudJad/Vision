# Database Seed Data

This directory contains JSON files for seeding the Vision PIM database with initial data.

## File Structure

The seed data files follow the dependency order:

1. **attributes.json** - Product attributes (e.g., color, size, name, description)
2. **attribute_options.json** - Options for select-type attributes (e.g., red, blue, S, M, L)
3. **families.json** - Product families that group attributes together
4. **family_variants.json** - Family variants defining variation axes
5. **categories.json** - Product categories (hierarchical)
6. **product_models.json** - Parent products (templates)
7. **products.json** - Specific product variants
8. **product_values.json** - Attribute values for products and product models

## Data Relationships

### Attributes → Attribute Options
- Attributes with type `simple_select` or `multi_select` have options
- Example: `color` attribute has options like "red", "blue", "black"

### Families → Attributes
- Families contain `attribute_ids` array
- These define which attributes are available for products in that family

### Family Variants → Families & Attributes
- Each variant belongs to a `family_id`
- `axes` array contains attribute IDs that vary between products (e.g., color, size)
- `attributes` array contains all attributes for the variant

### Product Models → Family Variants & Categories
- Product models link to `family_variant_id`
- Can have multiple `category_ids`
- Can have a `parent_id` for multi-level products

### Products → Product Models
- Each product has a `product_model_id`
- Products are specific variants (e.g., "Red T-Shirt in Size M")

### Product Values → Products/Product Models & Attributes
- Store actual attribute values for products and product models
- `entity_type` can be "product" or "product_model"
- `entity_id` references the product or product model
- `attribute_id` references which attribute this value is for
- `scope` and `locale` allow for channel and language-specific values

## Sample Data Included

### Attributes (8 total)
- **name** - Text, localizable (Product name)
- **description** - Textarea, localizable & scopable (Product description)
- **color** - Simple select (Red, Blue, Black, White)
- **size** - Simple select (XS, S, M, L, XL)
- **price** - Price, scopable (Product price)
- **weight** - Measurement (Product weight in kg)
- **brand** - Text (Brand name)
- **material** - Multi-select (Cotton, Polyester, Silk)

### Families (2 total)
- **clothing** - For apparel products
- **electronics** - For electronic devices

### Categories (4 total)
- Apparel
  - Men's Clothing
  - Women's Clothing
- Electronics

### Products
- Classic T-Shirt (3 variants: Red-M, Red-L, Blue-M)
- Summer Dress (2 variants: Black-S, Black-M)

## Usage

### Automatic Seeding
The database is automatically seeded when you run:
```bash
docker-compose up
```

The seeding runs after migrations and before the application starts.

### Manual Seeding
You can also run the seed script manually:

```bash
# Inside the container
docker-compose exec vision python seed_database.py

# Or with force flag to skip existing data check
docker-compose exec vision python seed_database.py --force
```

### Outside Docker
```bash
python seed_database.py
# or
python seed_database.py --force
```

## Customizing Seed Data

### Adding New Data
1. Edit the appropriate JSON file(s)
2. Ensure UUIDs are unique
3. Maintain referential integrity (IDs must match)
4. Restart the container or run the seed script manually

### UUID Format
All IDs must be valid UUIDs in the format: `550e8400-e29b-41d4-a716-446655440001`

### Important Notes
- The seed script checks for existing data and skips duplicates
- Use `--force` flag to reseed even if data exists
- Maintain the correct order when adding related data
- Ensure attribute types match their backend types:
  - `text`, `textarea` → `string`
  - `number`, `price`, `measurement` → `float`
  - `simple_select` → `option`
  - `multi_select` → `options`
  - `boolean` → `boolean`
  - `date` → `date`

## Entity Relationships Diagram

```
Attribute (1) ──→ (N) AttributeOption
    ↑
    │ (M)
    │
Family (1) ──→ (N) FamilyVariant
    ↑                    ↑
    │                    │ (1)
    │                    │
    └────────── ProductModel (1) ──→ (N) Product
                    ↑                        ↑
                    │ (N)                    │ (N)
                    │                        │
                    └───── ProductValue ─────┘
                                ↓ (1)
                           Attribute
```

## Locales Used
- `en_US` - English (United States)
- `ar_EG` - Arabic (Egypt)

## Scopes Used
- `ecommerce` - E-commerce channel
- `mobile` - Mobile app channel

Add more locales and scopes as needed in the product_values.json file.
