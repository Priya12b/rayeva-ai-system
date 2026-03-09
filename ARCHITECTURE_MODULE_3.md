# Module 3: AI Impact Reporting Generator
## Architecture & Implementation Guide

### Overview
The AI Impact Reporting Generator automatically calculates and communicates the environmental and social impact of products and orders. It transforms raw transaction data into compelling impact stories for customers and stakeholders.

### 1. Data Models

#### ImpactReport Model
```python
# app/models/impact_report.py
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from datetime import datetime
from app.database import Base

class ImpactReport(Base):
    __tablename__ = "impact_reports"

    id = Column(Integer, primary_key=True, index=True)
    
    # Data source
    order_id = Column(Integer, nullable=False, index=True)
    product_ids = Column(JSON)  # List of product IDs in order
    
    # Impact calculations
    plastic_saved_kg = Column(Float)
    carbon_avoided_kg = Column(Float)
    water_saved_liters = Column(Float)
    
    # Sourcing impact
    locally_sourced_percentage = Column(Float)
    fair_trade_items = Column(Integer)
    
    # AI-generated summaries
    impact_statement = Column(Text)  # Human-readable impact narrative
    action_items = Column(JSON)  # Suggested next actions for customer
    comparison_context = Column(Text)  # e.g., "This is equivalent to..."
    
    # Configuration
    carbon_methodology = Column(String)  # "EPA" or "IPCC"
    impact_scope = Column(String)  # "product" or "order"
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Carbon Emissions Database (reference data)
```python
# Store product-specific carbon footprints for calculations
class ProductCarbonFootprint(Base):
    __tablename__ = "product_carbon_footprints"
    
    id = Column(Integer, primary_key=True)
    product_category = Column(String)  # e.g., "Personal Care"
    production_carbon_kg = Column(Float)  # kg CO2 per unit
    packaging_carbon_kg = Column(Float)  # kg CO2 for packaging
    baseline_year = Column(Integer)  # Data year
```

### 2. AI Prompt Design

#### Impact Calculation Prompt
```
You are an environmental impact communication specialist. Calculate and communicate sustainability impact.

INPUT DATA:
- Product List: [name, category, sustainable_filters, quantity]
- Order Value: $XXX
- Baseline: Standard non-sustainable product impact

CALCULATE AND RETURN JSON:
{
    "plastic_saved_kg": <auto-calculated from filters>,
    "carbon_avoided_kg": <auto-calculated from production methods>,
    "water_saved_liters": <auto-calculated from material type>,
    "impact_statement": "Compelling 2-3 sentence narrative for customer",
    "action_items": ["actionable next step for customer"],
    "comparison_text": "This impact equals: X trees planted / Y hours of electricity for home"
}

METHODOLOGY:
1. Plastic saved: Count each "plastic-free" item as 0.15kg saved vs standard
2. Carbon: Factor from EPA product lifecycle data (avg 2.5kg CO2 per product)
3. Water: Vegan products save ~2000L vs conventional
4. Compostable items: +1.2x environmental benefit multiplier
5. Locally-sourced: Reduce carbon by 40% (shipping savings)

Make statements specific, measurable, and motivating.
```

### 3. API Endpoints

```python
# app/routers/impact.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/calculate-impact")
def calculate_order_impact(
    order_id: int,
    product_ids: List[int],
    db: Session = Depends(get_db)
):
    """
    Calculate and generate impact report for an order.
    
    Returns:
    {
        "plastic_saved_kg": float,
        "carbon_avoided_kg": float,
        "water_saved_liters": float,
        "impact_statement": str,
        "action_items": list,
        "comparison_text": str
    }
    """
    pass

@router.get("/impact-reports/{report_id}")
def get_impact_report(report_id: int, db: Session = Depends(get_db)):
    """Retrieve previously calculated impact report"""
    pass

@router.get("/customer-impact-summary/{customer_id}")
def get_customer_impact_summary(customer_id: int, db: Session = Depends(get_db)):
    """
    Aggregate impact across all customer purchases.
    
    Returns cumulative stats + monthly trend + peer comparison.
    """
    pass
```

### 4. Business Logic

#### Impact Calculation Engine
```python
# app/services/impact_service.py

def calculate_plastic_saved(products: List[Product]) -> float:
    """Calculate plastic saved in kg"""
    return len([p for p in products if "plastic-free" in p.sustainability_filters]) * 0.15

def calculate_carbon_avoided(products: List[Product]) -> float:
    """
    Calculate CO2 avoided in kg.
    Uses product carbon footprints from reference data.
    """
    total_carbon = 0
    for product in products:
        base_carbon = 2.5  # Default kg CO2
        
        # Adjustment factors
        if "recycled" in product.sustainability_filters:
            base_carbon *= 0.6  # 40% less carbon for recycled
        if "locally-sourced" in product.sustainability_filters:
            base_carbon *= 0.6  # 40% less due to transport
            
        total_carbon += base_carbon
    
    return total_carbon

def calculate_water_saved(products: List[Product]) -> float:
    """Calculate water saved in liters"""
    water_saved = 0
    for p in products:
        if "vegan" in p.sustainability_filters:
            water_saved += 2000
        if "organic" in p.sustainability_filters:
            water_saved += 800
    return water_saved
```

### 5. Key Features

✅ **Real-time Impact Calculation**
- Instant feedback on order impact
- Formula-based + AI-generated context

✅ **Peer Comparison**
- "You've saved more than X% of our customers this month"
- Motivate further sustainable purchasing

✅ **Monthly/Annual Reports**
- Customer dashboard showing impact trends
- Shareable social media summaries

✅ **Integration Points**
- Trigger after order completion
- Include in order confirmation email
- Display on customer account dashboard
- Publish customer testimonials with impact data

### 6. Testing Strategy

```python
# test_impact_service.py
def test_plastic_saved_calculation():
    products = [Product(sustainability_filters=["plastic-free"]) for _ in range(3)]
    assert calculate_plastic_saved(products) == 0.45  # 3 * 0.15

def test_carbon_avoided_with_factors():
    p = Product(sustainability_filters=["recycled", "locally-sourced"])
    # base 2.5 * 0.6 (recycled) * 0.6 (local) = 0.9 kg
    assert calculate_carbon_avoided([p]) == 0.9
```

### 7. Future Enhancements

- [ ] Third-party verification (Carbon Trust, Green Certifications)
- [ ] Blockchain impact attestation
- [ ] Integration with impact offsetting programs (Tree-Nation, etc.)
- [ ] Gamification (badges for sustainable milestones)
- [ ] Customer community features ("impact leaderboard")
