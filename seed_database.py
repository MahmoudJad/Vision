#!/usr/bin/env python3
"""
Database seeding script for Vision PIM
Loads initial data from JSON files in the data_seeds directory
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from uuid import UUID

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import AsyncSessionLocal
from src.model.attributes import Attribute, AttributeOption
from src.model.family import Family
from src.model.family_variants import FamilyVariant
from src.model.category import Category
from src.model.parent_product import ProductModel
from src.model.product import Product
from src.model.product_values import ProductValue
from src.enums.enum import AttributeType, BackendType, EntityType


class DatabaseSeeder:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.stats = {
            "attributes": 0,
            "attribute_options": 0,
            "families": 0,
            "family_variants": 0,
            "categories": 0,
            "product_models": 0,
            "products": 0,
            "product_values": 0
        }

    def load_json(self, filename: str):
        """Load JSON data from file"""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"⚠️  File not found: {filepath}")
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing {filename}: {e}")
            return []

    async def check_existing_data(self, db: AsyncSession) -> bool:
        """Check if database already has seed data"""
        result = await db.execute(select(Attribute))
        attributes = result.scalars().all()
        return len(attributes) > 0

    async def seed_attributes(self, db: AsyncSession):
        """Seed attributes"""
        print("📝 Seeding attributes...")
        data = self.load_json("attributes.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(Attribute).where(Attribute.code == item["code"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Attribute '{item['code']}' already exists, skipping")
                continue
            
            attribute = Attribute(
                id=UUID(item["id"]),
                code=item["code"],
                type=AttributeType[item["type"]],  # Use enum name instead of value
                backend_type=BackendType[item["backend_type"]],  # Use enum name instead of value
                is_localizable=item["is_localizable"],
                is_scopable=item["is_scopable"],
                group_code=item.get("group_code"),
                labels=item.get("labels"),
                config=item.get("config")
            )
            db.add(attribute)
            self.stats["attributes"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['attributes']} attributes")

    async def seed_attribute_options(self, db: AsyncSession):
        """Seed attribute options"""
        print("📝 Seeding attribute options...")
        data = self.load_json("attribute_options.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(AttributeOption).where(
                    AttributeOption.attribute_id == UUID(item["attribute_id"]),
                    AttributeOption.code == item["code"]
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Option '{item['code']}' already exists, skipping")
                continue
            
            option = AttributeOption(
                id=UUID(item["id"]),
                attribute_id=UUID(item["attribute_id"]),
                code=item["code"],
                labels=item.get("labels"),
                sort_order=item.get("sort_order")
            )
            db.add(option)
            self.stats["attribute_options"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['attribute_options']} attribute options")

    async def seed_families(self, db: AsyncSession):
        """Seed families"""
        print("📝 Seeding families...")
        data = self.load_json("families.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(Family).where(Family.code == item["code"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Family '{item['code']}' already exists, skipping")
                continue
            
            # Convert attribute_ids to UUIDs
            attribute_ids = [UUID(aid) for aid in item.get("attribute_ids", [])]
            
            family = Family(
                id=UUID(item["id"]),
                code=item["code"],
                attribute_ids=attribute_ids,
                labels=item.get("labels")
            )
            db.add(family)
            self.stats["families"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['families']} families")

    async def seed_family_variants(self, db: AsyncSession):
        """Seed family variants"""
        print("📝 Seeding family variants...")
        data = self.load_json("family_variants.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(FamilyVariant).where(FamilyVariant.code == item["code"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Family variant '{item['code']}' already exists, skipping")
                continue
            
            # Convert axes and attributes to UUIDs
            axes = [UUID(aid) for aid in item.get("axes", [])]
            attributes = [UUID(aid) for aid in item.get("attributes", [])]
            
            family_variant = FamilyVariant(
                id=UUID(item["id"]),
                family_id=UUID(item["family_id"]),
                code=item["code"],
                level=item.get("level"),
                axes=axes,
                attributes=attributes
            )
            db.add(family_variant)
            self.stats["family_variants"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['family_variants']} family variants")

    async def seed_categories(self, db: AsyncSession):
        """Seed categories"""
        print("📝 Seeding categories...")
        data = self.load_json("categories.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(Category).where(Category.name == item["name"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Category '{item['name']}' already exists, skipping")
                continue
            
            parent_id = UUID(item["parent_id"]) if item.get("parent_id") else None
            
            category = Category(
                id=UUID(item["id"]),
                name=item["name"],
                description=item.get("description"),
                parent_id=parent_id
            )
            db.add(category)
            self.stats["categories"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['categories']} categories")

    async def seed_product_models(self, db: AsyncSession):
        """Seed product models"""
        print("📝 Seeding product models...")
        data = self.load_json("product_models.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(ProductModel).where(ProductModel.code == item["code"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Product model '{item['code']}' already exists, skipping")
                continue
            
            # Convert category_ids to UUIDs
            category_ids = [UUID(cid) for cid in item.get("category_ids", [])]
            family_variant_id = UUID(item["family_variant_id"]) if item.get("family_variant_id") else None
            parent_id = UUID(item["parent_id"]) if item.get("parent_id") else None
            
            product_model = ProductModel(
                id=UUID(item["id"]),
                sku=item.get("sku"),
                title=item["title"],
                code=item["code"],
                family_variant_id=family_variant_id,
                parent_id=parent_id,
                category_ids=category_ids
            )
            db.add(product_model)
            self.stats["product_models"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['product_models']} product models")

    async def seed_products(self, db: AsyncSession):
        """Seed products"""
        print("📝 Seeding products...")
        data = self.load_json("products.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(Product).where(Product.sku == item["sku"])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  ⏭️  Product '{item['sku']}' already exists, skipping")
                continue
            
            product_model_id = UUID(item["product_model_id"]) if item.get("product_model_id") else None
            
            product = Product(
                id=UUID(item["id"]),
                sku=item["sku"],
                product_model_id=product_model_id,
                enabled=item.get("enabled", True)
            )
            db.add(product)
            self.stats["products"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['products']} products")

    async def seed_product_values(self, db: AsyncSession):
        """Seed product values"""
        print("📝 Seeding product values...")
        data = self.load_json("product_values.json")
        
        for item in data:
            # Check if already exists
            result = await db.execute(
                select(ProductValue).where(
                    ProductValue.entity_type == EntityType[item["entity_type"]],  # Use enum name
                    ProductValue.entity_id == UUID(item["entity_id"]),
                    ProductValue.attribute_id == UUID(item["attribute_id"]),
                    ProductValue.scope == item.get("scope"),
                    ProductValue.locale == item.get("locale")
                )
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                continue
            
            product_value = ProductValue(
                entity_type=EntityType[item["entity_type"]],  # Use enum name instead of value
                entity_id=UUID(item["entity_id"]),
                attribute_id=UUID(item["attribute_id"]),
                scope=item.get("scope"),
                locale=item.get("locale"),
                value=item.get("value")
            )
            db.add(product_value)
            self.stats["product_values"] += 1
        
        await db.commit()
        print(f"✅ Created {self.stats['product_values']} product values")

    async def run(self, force: bool = False):
        """Run the seeding process"""
        print("🌱 Starting database seeding...")
        print(f"📂 Data directory: {self.data_dir}")
        
        async with AsyncSessionLocal() as db:
            # Check if data already exists
            if not force and await self.check_existing_data(db):
                print("⚠️  Database already contains data.")
                print("   Use --force flag to seed anyway (duplicates will be skipped)")
                return
            
            try:
                # Seed in order of dependencies
                await self.seed_attributes(db)
                await self.seed_attribute_options(db)
                await self.seed_families(db)
                await self.seed_family_variants(db)
                await self.seed_categories(db)
                await self.seed_product_models(db)
                await self.seed_products(db)
                await self.seed_product_values(db)
                
                print("\n✨ Seeding completed successfully!")
                print("\n📊 Summary:")
                for key, value in self.stats.items():
                    print(f"   {key}: {value}")
                
            except Exception as e:
                print(f"\n❌ Error during seeding: {e}")
                await db.rollback()
                raise


async def main():
    """Main entry point"""
    # Get the project root directory
    project_root = Path(__file__).parent
    data_dir = project_root / "data_seeds"
    
    # Check if --force flag is provided
    force = "--force" in sys.argv
    
    # Create and run seeder
    seeder = DatabaseSeeder(data_dir)
    await seeder.run(force=force)


if __name__ == "__main__":
    asyncio.run(main())
