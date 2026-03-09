#!/usr/bin/env python3
"""
Demo script for Rayeva AI System - Shows key API calls for testing.

Usage:
    python demo_api.py

Make sure backend is running: uvicorn app.main:app --reload
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(response, title="Response"):
    """Pretty print API response"""
    try:
        data = response.json()
        print(f"{title}:")
        print(json.dumps(data, indent=2))
        print(f"(Status: {response.status_code})")
    except:
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")

def demo_category_generation():
    """Demo: AI Auto-Category & Tag Generator"""
    print_header("DEMO 1: AI Auto-Category & Tag Generator")
    
    products = [
        {
            "name": "Bamboo Toothbrush",
            "description": "Eco-friendly toothbrush made from sustainable bamboo with compostable packaging",
            "material": "bamboo",
            "base_price": 12.99
        },
        {
            "name": "Organic Cotton T-Shirt",
            "description": "100% organic cotton, naturally dyed, fair-trade certified shirt",
            "material": "organic cotton",
            "base_price": 24.99
        },
        {
            "name": "Cork Yoga Mat",
            "description": "Natural cork and rubber yoga mat, perfect for home yoga practice",
            "material": "cork",
            "base_price": 45.00
        }
    ]
    
    for product in products:
        print(f"📦 Processing: {product['name']}")
        print(f"   Material: {product['material']}")
        print(f"   Price: ${product['base_price']}\n")
        
        response = requests.post(
            f"{BASE_URL}/ai/generate-category",
            json=product,
            headers={"Content-Type": "application/json"}
        )
        
        print_response(response, "Generated Categories & Tags")
        print()


def demo_proposal_generation():
    """Demo: AI B2B Proposal Generator"""
    print_header("DEMO 2: AI B2B Proposal Generator")
    
    scenarios = [
        {
            "name": "Nonprofit (High Sustainability)",
            "data": {
                "client_type": "nonprofit",
                "budget": 500,
                "sustainability_priority": "high"
            }
        },
        {
            "name": "Retailer (Medium Budget)",
            "data": {
                "client_type": "retailer",
                "budget": 1000,
                "sustainability_priority": "medium"
            }
        },
        {
            "name": "Corporate (Large Budget)",
            "data": {
                "client_type": "corporate",
                "budget": 2500,
                "sustainability_priority": "high"
            }
        }
    ]
    
    for scenario in scenarios:
        print(f"🎯 Scenario: {scenario['name']}")
        print(f"   Budget: ${scenario['data']['budget']}")
        print(f"   Sustainability Priority: {scenario['data']['sustainability_priority'].title()}\n")
        
        response = requests.post(
            f"{BASE_URL}/ai/generate-proposal",
            json=scenario['data'],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generated proposal with {len(data['recommended_products'])} products:")
            print(f"   - Total Cost: ${data['total_cost']:.2f}")
            print(f"   - Budget Remaining: ${data['budget_remaining']:.2f}")
            print(f"   - Impact Statement: {data['impact_positioning_summary'][:80]}...\n")
            
            print("   Recommended Products:")
            for product in data['recommended_products'][:3]:  # Show first 3
                print(f"     • {product['product_name']} x{product['quantity']} = ${product['total_price']:.2f}")
            print()
        else:
            print_response(response, "Error")
            print()


def demo_api_info():
    """Demo: Show API documentation info"""
    print_header("API DOCUMENTATION")
    
    print("📚 Swagger UI: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("📚 OpenAPI Schema: http://localhost:8000/openapi.json")
    print()
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response, "Health Check")
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running!")
        print("   Start with: cd backend && uvicorn app.main:app --reload")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("  🌱 RAYEVA AI SYSTEM - DEMO SCRIPT 🌱")
    print("="*60)
    print("\nThis script demonstrates the key features of Rayeva AI System.")
    print("Make sure the backend is running before proceeding!\n")
    
    try:
        # Test connection
        print("Checking backend connection...", end="")
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
            print(" ✅\n")
        except requests.exceptions.ConnectionError:
            print(" ❌\n")
            print("❌ ERROR: Backend not running!")
            print("   Start the backend with:")
            print("   cd backend")
            print("   uvicorn app.main:app --reload")
            print("\n   Then run this script again.")
            return
        
        # Run demos
        demo_category_generation()
        time.sleep(1)  # Small delay between demos
        
        demo_proposal_generation()
        time.sleep(1)
        
        demo_api_info()
        
        print("\n" + "="*60)
        print("  ✅ DEMO COMPLETE!")
        print("="*60)
        print("\n📝 Check the database for logged AI interactions:")
        print("   sqlite3 backend/rayeva.db")
        print("   SELECT module_name, validated, created_at FROM ai_logs;")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
