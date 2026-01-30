# Vision PIM - Seed Data Structure Visualization

## Entity Relationship Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ATTRIBUTE LAYER                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Attributes (8)                    Attribute Options (12)            │
│  ┌──────────────┐                 ┌────────────────────┐            │
│  │ name         │                 │ Color Options:      │            │
│  │ description  │                 │  - red, blue        │            │
│  │ color        │◄────────────────┤  - black, white     │            │
│  │ size         │                 │                     │            │
│  │ price        │                 │ Size Options:       │            │
│  │ weight       │◄────────────────┤  - xs, s, m, l, xl  │            │
│  │ brand        │                 │                     │            │
│  │ material     │                 │ Material Options:   │            │
│  └──────────────┘                 │  - cotton, polyester│            │
│                                    │  - silk             │            │
│                                    └────────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FAMILY LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Families (2)              Family Variants (2)                       │
│  ┌──────────────┐         ┌──────────────────────┐                 │
│  │ clothing     │◄────────┤ clothing_color_size   │                 │
│  │              │         │  Axes: [color, size]  │                 │
│  │ [7 attrs]    │         │  Level: 2             │                 │
│  └──────────────┘         └──────────────────────┘                 │
│                                                                       │
│  ┌──────────────┐         ┌──────────────────────┐                 │
│  │ electronics  │◄────────┤ electronics_simple    │                 │
│  │              │         │  Axes: []             │                 │
│  │ [5 attrs]    │         │  Level: 1             │                 │
│  └──────────────┘         └──────────────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       CATEGORY LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│        Apparel                         Electronics                   │
│           │                                  │                       │
│           ├─── Men's Clothing               └─── (no children)      │
│           │                                                          │
│           └─── Women's Clothing                                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRODUCT MODEL LAYER                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Product Model: Classic T-Shirt                                     │
│  ┌─────────────────────────────────────────┐                        │
│  │ Code: classic_tshirt                     │                        │
│  │ SKU: PM-TSHIRT-001                       │                        │
│  │ Family Variant: clothing_color_size      │                        │
│  │ Category: Men's Clothing                 │                        │
│  │                                           │                        │
│  │ Product Values (Product Model):          │                        │
│  │  - name (en_US): "Classic T-Shirt"       │                        │
│  │  - name (ar_EG): "تيشيرت كلاسيكي"       │                        │
│  │  - description: "A comfortable..."       │                        │
│  │  - brand: "Generic Brand"                │                        │
│  └─────────────────────────────────────────┘                        │
│                      │                                               │
│                      ▼                                               │
│  ┌────────────────────────────────────────────────────┐            │
│  │            PRODUCT VARIANTS                        │            │
│  ├────────────────────────────────────────────────────┤            │
│  │                                                     │            │
│  │  Product 1: TSHIRT-RED-M                           │            │
│  │  ├─ color: Red                                     │            │
│  │  ├─ size: M                                        │            │
│  │  └─ price (ecommerce): $29.99                     │            │
│  │                                                     │            │
│  │  Product 2: TSHIRT-RED-L                           │            │
│  │  ├─ color: Red                                     │            │
│  │  ├─ size: L                                        │            │
│  │  └─ price (ecommerce): $29.99                     │            │
│  │                                                     │            │
│  │  Product 3: TSHIRT-BLUE-M                          │            │
│  │  ├─ color: Blue                                    │            │
│  │  ├─ size: M                                        │            │
│  │  └─ price (ecommerce): $29.99                     │            │
│  └────────────────────────────────────────────────────┘            │
│                                                                       │
│  Product Model: Summer Dress                                        │
│  ┌─────────────────────────────────────────┐                        │
│  │ Code: summer_dress                       │                        │
│  │ SKU: PM-DRESS-001                        │                        │
│  │ Family Variant: clothing_color_size      │                        │
│  │ Category: Women's Clothing               │                        │
│  │                                           │                        │
│  │ Product Values (Product Model):          │                        │
│  │  - name (en_US): "Summer Dress"          │                        │
│  │  - description: "Beautiful summer..."    │                        │
│  │  - brand: "Fashion Co"                   │                        │
│  └─────────────────────────────────────────┘                        │
│                      │                                               │
│                      ▼                                               │
│  ┌────────────────────────────────────────────────────┐            │
│  │            PRODUCT VARIANTS                        │            │
│  ├────────────────────────────────────────────────────┤            │
│  │                                                     │            │
│  │  Product 1: DRESS-BLACK-S                          │            │
│  │  ├─ color: Black                                   │            │
│  │  ├─ size: S                                        │            │
│  │  └─ price (ecommerce): $59.99                     │            │
│  │                                                     │            │
│  │  Product 2: DRESS-BLACK-M                          │            │
│  │  ├─ color: Black                                   │            │
│  │  ├─ size: M                                        │            │
│  │  └─ price (ecommerce): $59.99                     │            │
│  └────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow on Creation

```
1. CREATE ATTRIBUTES
   └─> Define structure: name, type, backend_type, flags
       └─> For select types: Add options

2. CREATE FAMILIES
   └─> Group attributes together
       └─> Define which attributes products in this family can have

3. CREATE FAMILY VARIANTS
   └─> Define variation axes (which attributes create variants)
       └─> Specify all attributes available at variant level

4. CREATE CATEGORIES
   └─> Organize products hierarchically
       └─> Can have parent-child relationships

5. CREATE PRODUCT MODELS
   └─> Template/parent for products
       └─> Link to family variant
       └─> Link to categories
       └─> Add common attribute values

6. CREATE PRODUCTS
   └─> Specific variants
       └─> Link to product model
       └─> Add variant-specific attributes (color, size)
       └─> Add scope-specific values (prices per channel)

7. CREATE PRODUCT VALUES
   └─> Store all attribute values
       └─> For product models: Common attributes
       └─> For products: Variant attributes
       └─> Support localization (locale)
       └─> Support channels (scope)
```

## Attribute Value Inheritance

```
Product Model (Classic T-Shirt)
    │
    ├─ Shared Attributes:
    │   ├─ name (inherited by all variants)
    │   ├─ description (inherited by all variants)
    │   └─ brand (inherited by all variants)
    │
    └─ Products (Variants)
        │
        ├─ TSHIRT-RED-M
        │   ├─ Inherited: name, description, brand
        │   └─ Specific: color=Red, size=M, price=$29.99
        │
        ├─ TSHIRT-RED-L
        │   ├─ Inherited: name, description, brand
        │   └─ Specific: color=Red, size=L, price=$29.99
        │
        └─ TSHIRT-BLUE-M
            ├─ Inherited: name, description, brand
            └─ Specific: color=Blue, size=M, price=$29.99
```

## Multi-Locale & Multi-Scope Support

```
Classic T-Shirt Product Model
│
├─ name (locale: en_US): "Classic T-Shirt"
├─ name (locale: ar_EG): "تيشيرت كلاسيكي"
│
└─ description (scope: ecommerce, locale: en_US): "A comfortable..."
    description (scope: mobile, locale: en_US): "Comfortable tee"
    description (scope: ecommerce, locale: ar_EG): "تيشيرت مريح..."

TSHIRT-RED-M Product
│
├─ price (scope: ecommerce): $29.99
├─ price (scope: wholesale): $19.99
└─ price (scope: mobile): $29.99
```

## Seeding Order (Dependencies)

```
    attributes.json
         ↓
    attribute_options.json
         ↓
    families.json
         ↓
    family_variants.json
         ↓
    categories.json
         ↓
    product_models.json
         ↓
    products.json
         ↓
    product_values.json
```

Each file depends on the data from files above it in the hierarchy.
