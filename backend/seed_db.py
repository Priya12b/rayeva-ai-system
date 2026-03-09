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
        "name": "Bamboo Toothbrush Set",
        "description": "Eco-friendly bamboo toothbrushes with compostable packaging and soft bristles",
        "material": "bamboo",
        "base_price": 12.99,
        "ai_primary_category": "Personal Care",
        "ai_sub_category": "Eco-friendly Oral Care",
        "seo_tags": ["bamboo-toothbrush", "eco-friendly", "compostable", "sustainable", "plastic-free", "vegan"],
        "sustainability_filters": ["plastic-free", "biodegradable", "vegan", "organic"]
    },
    {
        "name": "Organic Cotton T-Shirt",
        "description": "100% organic cotton unisex t-shirt, naturally dyed, zero-waste packaging",
        "material": "organic cotton",
        "base_price": 24.99,
        "ai_primary_category": "Fashion & Accessories",
        "ai_sub_category": "Sustainable Apparel",
        "seo_tags": ["organic-cotton", "sustainable-fashion", "eco-shirt", "fair-trade", "vegan"],
        "sustainability_filters": ["organic", "fair-trade", "vegan", "locally-sourced"]
    },
    {
        "name": "Reusable Stainless Steel Water Bottle",
        "description": "Double-walled vacuum insulated water bottle, keeps drinks cold for 24hr or hot for 12hr",
        "material": "recycled stainless steel",
        "base_price": 35.00,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Sustainable Drinkware",
        "seo_tags": ["water-bottle", "stainless-steel", "reusable", "eco-friendly", "plastic-free"],
        "sustainability_filters": ["plastic-free", "recycled", "durable", "zero-waste"]
    },
    {
        "name": "Compostable Coffee Capsules (50-pack)",
        "description": "Biodegradable coffee capsules made from plant-based materials, compatible with Nespresso machines",
        "material": "compostable bioplastic",
        "base_price": 18.50,
        "ai_primary_category": "Food & Beverages",
        "ai_sub_category": "Sustainable Coffee",
        "seo_tags": ["coffee-capsules", "compostable", "eco-friendly", "organic", "fair-trade"],
        "sustainability_filters": ["compostable", "plastic-free", "organic", "fair-trade"]
    },
    {
        "name": "Cork Yoga Mat",
        "description": "Natural cork and natural rubber yoga mat, non-slip, eco-friendly, ultra lightweight",
        "material": "cork",
        "base_price": 45.00,
        "ai_primary_category": "Fitness & Sports",
        "ai_sub_category": "Sustainable Fitness",
        "seo_tags": ["yoga-mat", "cork", "eco-friendly", "natural", "sustainable"],
        "sustainability_filters": ["biodegradable", "locally-sourced", "vegan", "natural"]
    },
    {
        "name": "Recycled Plastic Storage Containers (Set of 3)",
        "description": "Durable food storage containers made from 100% recycled post-consumer plastic",
        "material": "recycled plastic",
        "base_price": 22.99,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Sustainable Storage",
        "seo_tags": ["storage-containers", "recycled", "plastic", "durable", "eco-friendly"],
        "sustainability_filters": ["recycled", "durable", "plastic-free"]
    },
    {
        "name": "Wooden Bamboo Utensil Set",
        "description": "Portable utensil set including fork, spoon, and knife made from bamboo",
        "material": "bamboo",
        "base_price": 8.99,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Eco-friendly Kitchenware",
        "seo_tags": ["utensils", "bamboo", "portable", "eco-friendly", "plastic-free", "travel"],
        "sustainability_filters": ["plastic-free", "biodegradable", "vegan"]
    },
    {
        "name": "Organic Bamboo Skincare Set",
        "description": "Complete skincare set with face wash, moisturizer, and serum in bamboo packaging",
        "material": "bamboo",
        "base_price": 42.00,
        "ai_primary_category": "Personal Care",
        "ai_sub_category": "Organic Skincare",
        "seo_tags": ["skincare", "organic", "bamboo", "eco-friendly", "vegan", "cruelty-free"],
        "sustainability_filters": ["organic", "plastic-free", "vegan", "fair-trade"]
    },
    {
        "name": "Recycled Paper Notebook (100 pages)",
        "description": "Eco-friendly notebook made from 100% recycled paper, perfect for journaling or note-taking",
        "material": "recycled paper",
        "base_price": 9.99,
        "ai_primary_category": "Office & School",
        "ai_sub_category": "Sustainable Stationery",
        "seo_tags": ["notebook", "recycled", "paper", "eco-friendly", "sustainable"],
        "sustainability_filters": ["recycled", "biodegradable"]
    },
    {
        "name": "Natural Linen Bed Sheets (Queen Size)",
        "description": "100% pure linen bed sheets, naturally temperature regulating, very durable",
        "material": "linen",
        "base_price": 89.99,
        "ai_primary_category": "Home & Kitchen",
        "ai_sub_category": "Sustainable Bedding",
        "seo_tags": ["bed-sheets", "linen", "organic", "sustainable", "durable", "natural"],
        "sustainability_filters": ["organic", "biodegradable", "locally-sourced", "durable"]
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


def seed_database():
    """Populate database with sample data"""
    db = SessionLocal()
    
    try:
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
    seed_database()
