import json
import logging
from sqlalchemy.orm import Session
from app.models.ai_log import AILog

logger = logging.getLogger(__name__)

# Allowed sustainability filters
SUSTAINABILITY_FILTERS = [
    "plastic-free",
    "compostable",
    "vegan",
    "recycled",
    "biodegradable",
    "locally-sourced",
    "organic",
    "fair-trade"
]

# Simple category keyword mapping
CATEGORY_KEYWORDS = {
    "Personal Care": ["toothbrush", "soap", "shampoo", "lotion"],
    "Home & Kitchen": ["kitchen", "dish", "container", "utensil"],
    "Fashion": ["shirt", "clothing", "bag", "fashion"],
    "Food & Beverages": ["food", "tea", "coffee", "snack"],
    "Electronics": ["phone", "charger", "device"],
    "Fitness": ["yoga", "gym", "fitness"],
}


def determine_category(name: str, description: str, material: str):
    text = f"{name} {description} {material}".lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Home & Kitchen"


def determine_sustainability(material: str, description: str):
    material = material.lower()
    description = description.lower()

    filters = []

    if "bamboo" in material:
        filters += ["plastic-free", "biodegradable"]

    if "recycled" in material:
        filters.append("recycled")

    if "organic" in description:
        filters.append("organic")

    if "vegan" in description:
        filters.append("vegan")

    filters = list(set(filters))

    if not filters:
        filters = ["plastic-free"]

    return filters


def generate_seo_tags(name: str, description: str):
    tags = set()

    words = name.lower().split()
    for w in words:
        if len(w) > 3:
            tags.add(w)

    desc_words = description.lower().split()
    for w in desc_words:
        if len(w) > 4:
            tags.add(w)

    tags.add("eco-friendly")
    tags.add("sustainable")

    return list(tags)[:8]


# -------------------------------------------------------
# AI CATEGORY GENERATOR
# -------------------------------------------------------

def generate_category_tags(product_data: dict, db: Session):

    prompt = f"""
Classify the product and generate SEO tags.

Name: {product_data['name']}
Description: {product_data['description']}
Material: {product_data['material']}
Price: {product_data['base_price']}
"""

    try:

        category = determine_category(
            product_data["name"],
            product_data["description"],
            product_data["material"]
        )

        filters = determine_sustainability(
            product_data["material"],
            product_data["description"]
        )

        seo_tags = generate_seo_tags(
            product_data["name"],
            product_data["description"]
        )

        ai_response = {
            "primary_category": category,
            "sub_category": f"Sustainable {category}",
            "seo_tags": seo_tags,
            "sustainability_filters": filters
        }

        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=json.dumps(ai_response),
            validated=True
        )

        db.add(log)
        db.commit()

        return ai_response

    except Exception as e:

        logger.error(f"Category generation error: {str(e)}")

        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=str(e),
            validated=False
        )

        db.add(log)
        db.commit()

        raise


# -------------------------------------------------------
# AI B2B PROPOSAL GENERATOR
# -------------------------------------------------------

def generate_proposal(client_type, budget, sustainability_priority, products, db: Session):

    prompt = f"""
Generate B2B proposal

Client type: {client_type}
Budget: {budget}
Sustainability priority: {sustainability_priority}
"""

    try:

        remaining_budget = float(budget)
        total_cost = 0
        recommendations = []

        for p in products:

            if p.base_price is None:
                continue

            if remaining_budget < p.base_price:
                continue

            # Calculate reasonable quantity (not all possible units)
            max_qty = int(remaining_budget / p.base_price)
            min_qty = max(1, int(budget / (p.base_price * 5)))  # Aim for 5+ product types
            qty = min(max_qty, min_qty)

            if qty <= 0:
                continue

            cost = qty * p.base_price

            if total_cost + cost > budget * 0.95:  # Allow up to 95% of budget
                continue

            recommendations.append({
                "product_id": p.id,
                "product_name": p.name,
                "quantity": qty,
                "unit_price": float(p.base_price),
                "total_price": float(cost),
                "sustainability_filters": p.sustainability_filters or []
            })

            total_cost += cost
            remaining_budget -= cost

        impact_text = "This proposal focuses on sustainable products that reduce environmental impact."

        if client_type.lower() == "hotel":
            impact_text = "These eco-friendly products support sustainable hospitality operations."

        if client_type.lower() == "retailer":
            impact_text = "Products selected to attract sustainability-conscious consumers."

        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=json.dumps({
                "recommendations": len(recommendations),
                "total_cost": total_cost
            }),
            validated=True
        )

        db.add(log)
        db.commit()

        return {
            "recommended_products": recommendations,
            "total_cost": float(total_cost),
            "budget_remaining": float(budget - total_cost),
            "impact_positioning_summary": impact_text,
            "business_rationale": "Optimized for sustainability and budget utilization"
        }

    except Exception as e:

        logger.error(f"Proposal generation error: {str(e)}")

        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=str(e),
            validated=False
        )

        db.add(log)
        db.commit()

        raise