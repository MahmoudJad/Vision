# Vision
Vision is the Product Information Management (PIM) microservice in the e-commerce ecosystem. It serves as the single source of truth for product-related data — defining, structuring, and maintaining the attributes, categories, and hierarchies that shape every product in the catalog. 

# 🧠 Vision — Product Information Management (PIM) Microservice

> “To see the world as it truly is.” — *Vision*

**Vision** is the PIM (Product Information Management) microservice responsible for defining, structuring, and managing all product information in the e-commerce ecosystem.

It acts as the *core intelligence layer* — ensuring every product is enriched with accurate attributes, properly categorized, and ready to be consumed by other services such as **Thiderman**, **Dragon**, and **Gachanger**.

---

## 🚀 Features

- 🗂 **Category Management**  
  Maintain a hierarchical product category tree with parent-child relationships.

- 🧱 **Attribute Management**  
  Define and manage attribute metadata such as name, type, scopable/localizable flags, and allowed options.

- 🧬 **Family & Variant Structures**  
  Create product families and family variants to define attribute sets and variant configurations.

- 📦 **Product Model Management**  
  Store and manage base product models used as templates for variant products.

- 🔍 **Validation Layer**  
  Ensure every product and variant fits within its assigned family and category rules.

- 🌐 **API-First Design**  
  Built with **FastAPI**, fully documented and OpenAPI-compliant.

- 🧾 **Database**  
  Supports both **PostgreSQL** (production) and **SQLite** (development/testing).

---

## 🏗️ Architecture Overview

Vision fits into the distributed system as follows:

## 🐳 Docker Setup

### Prerequisites
- Docker and Docker Compose installed
- Git

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/MahmoudJad/Vision.git
   cd Vision
   ```

2. **Start the services**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```
   
   The startup process will automatically:
   - Run database migrations
   - Seed the database with initial data
   - Start the FastAPI application

3. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050 (admin@admin.com / root)

### Docker Services

- **vision**: Main FastAPI application (port 8000)
- **dev_db**: PostgreSQL development database (port 5432)
- **test_db**: PostgreSQL test database (port 5433)
- **pgadmin**: Database administration interface (port 5050)

### Environment Configuration

The application uses environment variables defined in `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://db_user:db_password@dev_db:5432/dev_db
TEST_DATABASE_URL=postgresql+asyncpg://db_user:db_password@test_db:5432/test_db

# Application Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

---

## 🌱 Database Seeding

Vision includes a comprehensive database seeding system with sample data for testing and development.

### Automatic Seeding

The database is automatically seeded when you run `docker-compose up`. The seed data includes:

- **8 Attributes** (name, description, color, size, price, weight, brand, material)
- **12 Attribute Options** (color options, size options, material options)
- **2 Families** (clothing, electronics)
- **2 Family Variants** (clothing with color/size variations, electronics simple)
- **4 Categories** (Apparel → Men's/Women's Clothing, Electronics)
- **2 Product Models** (Classic T-Shirt, Summer Dress)
- **5 Products** (T-shirt variants in different colors/sizes, Dress variants)
- **Product Values** (Localized names, descriptions, prices, and variant-specific attributes)

### Manual Seeding

```bash
# Seed the database manually
docker-compose exec vision python seed_database.py

# Force reseed (skip duplicate checks)
docker-compose exec vision python seed_database.py --force

# Reset database and reseed from scratch
docker-compose exec vision bash reset_and_seed.sh
```

### Seed Data Location

All seed data is stored in JSON files in the `data_seeds/` directory:
- `attributes.json`
- `attribute_options.json`
- `families.json`
- `family_variants.json`
- `categories.json`
- `product_models.json`
- `products.json`
- `product_values.json`

See [data_seeds/README.md](data_seeds/README.md) for detailed documentation on customizing seed data.

---

## 🛠️ Development Commands

```bash
# View logs
docker-compose -f docker/docker-compose.yml logs -f vision

# Run tests
docker-compose -f docker/docker-compose.yml exec vision pytest

# Access shell
docker-compose -f docker/docker-compose.yml exec vision bash

# Stop services
docker-compose -f docker/docker-compose.yml down

# Rebuild and restart
docker-compose -f docker/docker-compose.yml up --build -d

# Create a new migration file 
docker-compose -f docker/docker-compose.yml exec vision alembic revision --autogenerate -m "migration file name"

# Apply the new migration 
docker-compose -f docker/docker-compose.yml exec vision alembic upgrade head

# Seed database
docker-compose -f docker/docker-compose.yml exec vision python seed_database.py

# Reset and reseed database
docker-compose -f docker/docker-compose.yml exec vision bash reset_and_seed.sh
```
