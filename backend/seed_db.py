"""
Database seed script - populates with sample sustainable products.

Usage:
    python seed_db.py

This creates sample products so the API has data to work with for demos.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.product import Product
from app.models.ai_log import AILog
import json
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

# Sample products
PRODUCTS = [
    {
        "name": "Rayeva Wooden Water Bottle",
        "description": "Premium handcrafted wooden water bottle with bamboo exterior and food-grade stainless steel inner lining",
        "material": "bamboo",
        "base_price": 799.00,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Sustainable Drinkware",
        "seo_tags": ["wooden-water-bottle", "bamboo", "reusable", "eco-friendly", "sustainable"],
        "sustainability_filters": ["plastic-free", "vegan", "organic"]
    },
    {
        "name": "Beeswax Food Wraps",
        "description": "Set of 3 reusable food wraps made from beeswax and cotton",
        "material": "beeswax and cotton",
        "base_price": 449.00,
        "ai_primary_category": "Sustainable Packaging",
        "ai_sub_category": "Reusable Food Storage",
        "seo_tags": ["beeswax-wrap", "reusable-wrap", "plastic-free", "food-storage", "eco-kitchen"],
        "sustainability_filters": ["plastic-free", "biodegradable", "organic"]
    },
    {
        "name": "Organic Hemp Seed Body Oil",
        "description": "Cold-pressed organic hemp seed oil rich in Omega-3 and Omega-6",
        "material": "hemp seed oil",
        "base_price": 599.00,
        "ai_primary_category": "Beauty & Personal Care",
        "ai_sub_category": "Organic Skincare",
        "seo_tags": ["hemp-seed-oil", "body-oil", "organic-skincare", "cold-pressed", "natural"],
        "sustainability_filters": ["organic", "vegan", "non-toxic"]
    },
    {
        "name": "Coconut Shell Bowls Set",
        "description": "Handcrafted bowl set made from recycled coconut shells",
        "material": "recycled coconut shell",
        "base_price": 699.00,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Eco-friendly Kitchenware",
        "seo_tags": ["coconut-bowl", "handcrafted", "recycled", "zero-waste", "kitchenware"],
        "sustainability_filters": ["recycled", "biodegradable", "handmade"]
    },
    {
        "name": "Recycled Glass Tumblers",
        "description": "Set of 4 tumblers made from 100% recycled glass",
        "material": "recycled glass",
        "base_price": 799.00,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Sustainable Drinkware",
        "seo_tags": ["recycled-glass", "tumblers", "drinkware", "eco-friendly", "kitchen"],
        "sustainability_filters": ["recycled", "plastic-free", "durable"]
    },
    {
        "name": "Bamboo Toothbrush",
        "description": "Compostable bamboo toothbrush for daily oral care",
        "material": "bamboo",
        "base_price": 149.00,
        "ai_primary_category": "Beauty & Personal Care",
        "ai_sub_category": "Eco-friendly Oral Care",
        "seo_tags": ["bamboo-toothbrush", "oral-care", "plastic-free", "eco-friendly", "compostable"],
        "sustainability_filters": ["plastic-free", "biodegradable", "vegan"]
    },
    {
        "name": "Bamboo Cutlery Set",
        "description": "Portable reusable fork, spoon, and knife set made from bamboo",
        "material": "bamboo",
        "base_price": 299.00,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Eco-friendly Kitchenware",
        "seo_tags": ["bamboo-cutlery", "reusable", "travel-cutlery", "plastic-free", "zero-waste"],
        "sustainability_filters": ["plastic-free", "biodegradable", "vegan", "durable"]
    },
    {
        "name": "Organic Cotton Bag",
        "description": "Reusable organic cotton carry bag for groceries and daily essentials",
        "material": "organic cotton",
        "base_price": 249.00,
        "ai_primary_category": "Zero-Waste & Everyday Essentials",
        "ai_sub_category": "Reusable Bags",
        "seo_tags": ["organic-cotton-bag", "reusable-bag", "zero-waste", "grocery-bag", "eco-friendly"],
        "sustainability_filters": ["organic", "plastic-free", "reusable", "locally-sourced"]
    },
    {
        "name": "Eco-friendly Soap",
        "description": "Plant-based non-toxic bathing soap with minimal packaging",
        "material": "plant-based oils",
        "base_price": 199.00,
        "ai_primary_category": "Beauty & Personal Care",
        "ai_sub_category": "Natural Bath Care",
        "seo_tags": ["eco-soap", "plant-based", "non-toxic", "natural-care", "sustainable"],
        "sustainability_filters": ["non-toxic", "biodegradable", "vegan"]
    },
    {
        "name": "Rayeva Starter Kit",
        "description": "Starter bundle including bamboo toothbrush, reusable bottle, organic cotton bag, shaker, soap, and bamboo cutlery",
        "material": "mixed sustainable materials",
        "base_price": 499.00,
        "ai_primary_category": "Conscious Gifting",
        "ai_sub_category": "Sustainable Starter Kits",
        "seo_tags": ["starter-kit", "eco-bundle", "gift-set", "zero-waste", "sustainable-living"],
        "sustainability_filters": ["plastic-free", "vegan", "organic", "ethical-labour"]
    }
]

# Sample AI logs showing successful categorization
SAMPLE_LOGS = [
    {
        "module_name": "category_generator",
        "prompt": "Classify product: Bamboo Toothbrush...",
        "response": json.dumps({
            "primary_category": "Personal Care",
            "sub_category": "Eco-friendly Oral Care",
            "seo_tags": ["bamboo-toothbrush", "eco-friendly", "compostable"]
        }),
        "validated": True
    },
    {
        "module_name": "proposal_generator",
        "prompt": "Generate proposal for nonprofit with budget $1000, high sustainability priority...",
        "response": json.dumps({
            "recommendations": 5,
            "total_cost": 895.50,
            "impact_positioning": "This proposal maximizes social impact..."
        }),
        "validated": True
    }
]


def seed_database(reset=True):
    """Populate database with sample data.

    Args:
        reset: If True, clear existing data before inserting samples.
    """
    db = SessionLocal()
    
    try:
        existing_count = db.query(Product).count()

        # For startup seeding on free hosting, avoid destructive reset by default.
        if not reset and existing_count > 0:
            print(f"✓ Seed skipped: database already has {existing_count} products")
            return

        if reset:
            # Clear existing data (optional)
            db.query(Product).delete()
            db.query(AILog).delete()
            db.commit()
        
        # Add products
        print("Adding sample products...")
        for product_data in PRODUCTS:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print(f"✓ Added {len(PRODUCTS)} products")
        
        # Add sample AI logs
        print("Adding sample AI logs...")
        for log_data in SAMPLE_LOGS:
            log = AILog(
                **log_data,
                created_at=datetime.utcnow()
            )
            db.add(log)
        
        db.commit()
        print(f"✓ Added {len(SAMPLE_LOGS)} AI logs")
        
        print("\n✅ Database seeding complete!")
        print(f"   - {len(PRODUCTS)} products ready")
        print(f"   - {len(SAMPLE_LOGS)} AI logs for audit trail")
        print("\n   You can now test the API with real data.")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database(reset=True)
