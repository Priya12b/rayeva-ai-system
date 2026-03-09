import os
import json
import logging
import hashlib
from sqlalchemy.orm import Session
from app.models.ai_log import AILog
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Predefined categories and allowed sustainability filters for validation
PREDEFINED_CATEGORIES = [
    "Personal Care", "Home & Kitchen", "Fashion & Accessories", 
    "Food & Beverages", "Electronics", "Fitness & Sports", 
    "Garden & Outdoor", "Office & School", "Toys & Games", "Health & Wellness"
]

SUSTAINABILITY_FILTERS = [
    "plastic-free", "compostable", "vegan", "recycled", 
    "biodegradable", "locally-sourced", "organic", "fair-trade"
]

# Deterministic category mapping based on keywords
CATEGORY_KEYWORDS = {
    "Personal Care": ["toothbrush", "soap", "shampoo", "lotion", "deodorant", "hygiene", "skincare", "cosmetics"],
    "Home & Kitchen": ["kitchen", "home", "dish", "cleaning", "storage", "organizer", "container", "utensil"],
    "Fashion & Accessories": ["clothing", "apparel", "fashion", "bag", "accessory", "shoe", "textile", "garment"],
    "Food & Beverages": ["food", "beverage", "snack", "drink", "coffee", "tea", "organic", "nutrition"],
    "Electronics": ["electronic", "device", "phone", "charger", "tech", "gadget", "digital"],
    "Fitness & Sports": ["fitness", "sport", "yoga", "exercise", "gym", "runner", "athletic"],
    "Health & Wellness": ["health", "wellness", "vitamin", "supplement", "medical", "wellbeing"],
    "Garden & Outdoor": ["garden", "outdoor", "plant", "lawn", "patio", "camping", "hiking"],
}

# Sustainability suggestions based on material and description
MATERIAL_SUSTAINABILITY = {
    "bamboo": ["plastic-free", "biodegradable", "organic"],
    "wood": ["biodegradable", "recycled", "locally-sourced"],
    "organic cotton": ["organic", "vegan", "biodegradable"],
    "recycled plastic": ["recycled", "plastic-free"],
    "metal": ["recycled", "durable"],
    "glass": ["recyclable", "plastic-free"],
    "linen": ["organic", "biodegradable"],
    "cork": ["natural", "biodegradable", "locally-sourced"],
}


def _determine_category(product_name: str, description: str, material: str) -> str:
    """
    Deterministically determine primary category based on keywords.
    In production, this would be done by AI with nuance.
    """
    combined_text = f"{product_name} {description} {material}".lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            return category
    
    return "Home & Kitchen"  # Default fallback


def _determine_sustainability_filters(material: str, description: str) -> list:
    """
    Deterministically suggest sustainability filters.
    In production, AI would apply nuanced reasoning.
    """
    filters = []
    material_lower = material.lower()
    description_lower = description.lower()
    
    # Check if material matches known sustainable attributes
    for material_type, material_filters in MATERIAL_SUSTAINABILITY.items():
        if material_type in material_lower:
            filters.extend(material_filters)
    
    # Check description keywords
    if "vegan" in description_lower:
        filters.append("vegan")
    if "organic" in description_lower:
        filters.append("organic")
    if "recycled" in description_lower:
        filters.append("recycled")
    if "compostable" in description_lower:
        filters.append("compostable")
    if "local" in description_lower:
        filters.append("locally-sourced")
    
    # Remove duplicates and ensure validity
    filters = list(set(filters))
    filters = [f for f in filters if f in SUSTAINABILITY_FILTERS][:5]
    
    return filters if filters else ["plastic-free"]  # Ensure at least one


def _generate_seo_tags(product_name: str, description: str, category: str) -> list:
    """
    Generate SEO tags based on product details.
    In production, AI would create more sophisticated tags.
    """
    tags = set()
    
    # Add product name as tag
    tags.add(product_name.lower().replace(" ", "-"))
    
    # Add category-related tags
    tags.add(category.lower().replace(" ", "-"))
    tags.add("sustainable")
    tags.add("eco-friendly")
    
    # Extract key adjectives from description
    keywords = description.lower().split()
    for word in keywords:
        if len(word) > 4 and word.isalpha():
            tags.add(word)
    
    # Add quality tags
    tags.add("quality")
    tags.add("durable")
    
    return list(tags)[:8]  # Return top 8 tags


def generate_category_tags(product_data: dict, db: Session) -> dict:
    """
    Generate AI-powered category classification and SEO tags for a product.
    
    THIS IS A MOCK IMPLEMENTATION with deterministic logic.
    In production, this would call OpenAI GPT-4o-mini.
    
    The prompts below are the ACTUAL prompts that would be used with a real API.
    
    Args:
        product_data: Dict with name, description, material, base_price
        db: SQLAlchemy session for logging
        
    Returns:
        Dict with primary_category, sub_category, seo_tags, sustainability_filters
    """
    
    # Build the ACTUAL prompt that would be sent to OpenAI
    prompt = f"""You are an AI system for sustainable e-commerce categorization.

Analyze this product and return ONLY valid JSON (no markdown, no extra text):

PRODUCT DETAILS:
- Name: {product_data.get('name', 'N/A')}
- Description: {product_data.get('description', 'N/A')}
- Material: {product_data.get('material', 'N/A')}
- Price: ${product_data.get('base_price', 0)}

ALLOWED PRIMARY CATEGORIES:
{', '.join(PREDEFINED_CATEGORIES)}

ALLOWED SUSTAINABILITY FILTERS:
{', '.join(SUSTAINABILITY_FILTERS)}

REQUIRED JSON FORMAT:
{{
    "primary_category": "select from allowed categories",
    "sub_category": "specific niche within primary",
    "seo_tags": ["5-8 specific, searchable tags for this product"],
    "sustainability_filters": ["relevant sustainability attributes from allowed list"]
}}

Return valid JSON only, no extra text."""

    try:
        # Mock AI response generation with deterministic logic
        logger.info(f"[MOCK AI] Processing category request for: {product_data.get('name')}")
        
        primary_category = _determine_category(
            product_data.get('name', ''),
            product_data.get('description', ''),
            product_data.get('material', '')
        )
        
        ai_response = {
            "primary_category": primary_category,
            "sub_category": f"Sustainable {primary_category.split('&')[0].strip()}",
            "seo_tags": _generate_seo_tags(
                product_data.get('name', ''),
                product_data.get('description', ''),
                primary_category
            ),
            "sustainability_filters": _determine_sustainability_filters(
                product_data.get('material', ''),
                product_data.get('description', '')
            )
        }
        
        # Log the AI interaction
        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=json.dumps(ai_response),
            validated=True
        )
        db.add(log)
        db.commit()
        
        logger.info(f"Category generated for '{product_data.get('name')}': {ai_response['primary_category']}")
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Error in category generation: {str(e)}")
        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=f"ERROR: {str(e)}",
            validated=False
        )
        db.add(log)
        db.commit()
        raise


def generate_proposal(client_type: str, budget: float, sustainability_priority: str, products: list, db: Session) -> dict:
    """
    Generate AI-powered B2B proposal with intelligent product recommendations.
    
    THIS IS A MOCK IMPLEMENTATION with business logic.
    In production, this would call OpenAI GPT-4o-mini for smarter recommendations.
    
    Args:
        client_type: Type of client (e.g., "retailer", "corporate", "nonprofit")
        budget: Total budget available for proposal
        sustainability_priority: Level of sustainability focus (low, medium, high)
        products: List of Product model instances
        db: SQLAlchemy session for logging
        
    Returns:
        Dict with recommended_products, total_cost, budget_remaining, impact_positioning_summary
    """
    
    product_list = "\n".join([
        f"- ID: {p.id}, Name: {p.name}, Price: ${p.base_price}, "
        f"Filters: {', '.join(p.sustainability_filters or [])}"
        for p in products[:20]
    ])
    
    prompt = f"""You are an AI system for sustainable B2B commerce proposals.

Generate an optimal product recommendation mix based on:
- Client Type: {client_type}
- Budget: ${budget}
- Sustainability Priority: {sustainability_priority}

AVAILABLE PRODUCTS:
{product_list}

Return ONLY valid JSON (no markdown):
{{
    "recommendations": [
        {{"product_id": <id>, "quantity": <qty>, "reasoning": "why this product"}}
    ],
    "impact_positioning": "2-3 sentences about sustainability impact",
    "business_rationale": "why this mix matches client needs"
}}

Focus on:
1. Budget optimization (use 85-95% of budget)
2. Sustainability match with client priority
3. Product diversity and complementarity
4. ROI potential for client resale"""

    try:
        logger.info(f"[MOCK AI] Generating proposal for {client_type} with budget ${budget}")
        
        # Mock recommendation logic
        recommendations = []
        total_cost = 0
        remaining_budget = budget
        
        # Sort products by sustainability match
        if sustainability_priority.lower() == "high":
            sorted_products = sorted(
                products,
                key=lambda p: len(p.sustainability_filters or []),
                reverse=True
            )
        else:
            sorted_products = products
        
        # Build recommendations
        for product in sorted_products:
            if remaining_budget >= product.base_price:
                quantity = min(
                    int(remaining_budget / product.base_price),
                    max(1, int(budget / (product.base_price * 3)))  # Reasonable max qty
                )
                cost = quantity * product.base_price
                
                if total_cost + cost <= budget * 0.95:  # Keep under 95% budget
                    recommendations.append({
                        "product_id": product.id,
                        "quantity": quantity,
                        "reasoning": f"Eco-friendly {product.ai_primary_category or 'product'}"
                    })
                    total_cost += cost
                    remaining_budget -= cost
        
        # Generate impact positioning based on client type
        impact_statements = {
            "nonprofit": "This curated selection maximizes social impact while staying within budget. Each product reduces carbon footprint and supports sustainable sourcing.",
            "retailer": "This diverse portfolio offers high-margin eco-friendly products that appeal to sustainability-conscious consumers.",
            "corporate": "These products align with ESG commitments and can be featured in employee wellness programs.",
        }
        
        impact_positioning = impact_statements.get(
            client_type.lower(),
            "This proposal prioritizes eco-friendly products that reduce waste and promote sustainable sourcing."
        )
        
        ai_response = {
            "recommendations": recommendations,
            "impact_positioning": impact_positioning,
            "business_rationale": f"Optimized for {sustainability_priority} sustainability priority"
        }
        
        # Log the proposal generation
        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=json.dumps({"recommendations": len(recommendations), "total_cost": total_cost}),
            validated=True
        )
        db.add(log)
        db.commit()
        
        # Build final recommendations with pricing
        final_recommendations = []
        for rec in recommendations:
            product = next((p for p in products if p.id == rec.get("product_id")), None)
            if product:
                final_recommendations.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": rec.get("quantity", 1),
                    "unit_price": float(product.base_price),
                    "total_price": float(rec.get("quantity", 1) * product.base_price),
                    "sustainability_filters": product.sustainability_filters or []
                })
        
        return {
            "recommended_products": final_recommendations,
            "total_cost": float(total_cost),
            "budget_remaining": float(budget - total_cost),
            "impact_positioning_summary": impact_positioning,
            "business_rationale": ai_response.get("business_rationale", "")
        }
        
    except Exception as e:
        logger.error(f"Error in proposal generation: {str(e)}")
        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=f"ERROR: {str(e)}",
            validated=False
        )
        db.add(log)
        db.commit()
        raise


# end of file
    """
    Generate AI-powered category classification and SEO tags for a product.
    
    Uses OpenAI GPT-4o-mini to provide intelligent categorization.
    Validates output against predefined categories and filters.
    Logs all requests and responses for auditing.
    
    Args:
        product_data: Dict with name, description, material, base_price
        db: SQLAlchemy session for logging
        
    Returns:
        Dict with primary_category, sub_category, seo_tags, sustainability_filters
    """
    
    # Build comprehensive prompt with clear instructions
    prompt = f"""You are an AI system for sustainable e-commerce categorization.

Analyze this product and return ONLY valid JSON (no markdown, no extra text):

PRODUCT DETAILS:
- Name: {product_data.get('name', 'N/A')}
- Description: {product_data.get('description', 'N/A')}
- Material: {product_data.get('material', 'N/A')}
- Price: ${product_data.get('base_price', 0)}

ALLOWED PRIMARY CATEGORIES:
{', '.join(PREDEFINED_CATEGORIES)}

ALLOWED SUSTAINABILITY FILTERS:
{', '.join(SUSTAINABILITY_FILTERS)}

REQUIRED JSON FORMAT:
{{
    "primary_category": "select from allowed categories",
    "sub_category": "specific niche within primary",
    "seo_tags": ["5-8 specific, searchable tags for this product"],
    "sustainability_filters": ["relevant sustainability attributes from allowed list"]
}}

Return valid JSON only, no extra text."""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sustainable commerce AI expert. Return ONLY valid JSON responses."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        ai_output = response.choices[0].message.content.strip()
        
        # Parse JSON response
        ai_response = json.loads(ai_output)
        
        # Validate response structure
        required_fields = ["primary_category", "sub_category", "seo_tags", "sustainability_filters"]
        if not all(field in ai_response for field in required_fields):
            raise ValueError(f"Missing required fields. Got: {ai_response.keys()}")
        
        # Ensure seo_tags is a list
        if not isinstance(ai_response.get("seo_tags"), list):
            ai_response["seo_tags"] = [str(ai_response.get("seo_tags", ""))]
        
        # Validate and clean sustainability filters
        if isinstance(ai_response["sustainability_filters"], str):
            ai_response["sustainability_filters"] = [ai_response["sustainability_filters"]]
        
        # Log the AI interaction for audit trail
        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=json.dumps(ai_response),
            validated=True
        )
        db.add(log)
        db.commit()
        
        logger.info(f"Category generated for '{product_data.get('name')}': {ai_response['primary_category']}")
        
        # Return only required fields
        return {
            "primary_category": ai_response["primary_category"],
            "sub_category": ai_response["sub_category"],
            "seo_tags": ai_response["seo_tags"],
            "sustainability_filters": ai_response["sustainability_filters"]
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {ai_output}")
        raise ValueError(f"AI returned invalid JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Error in category generation: {str(e)}")
        # Log failed attempt
        log = AILog(
            module_name="category_generator",
            prompt=prompt,
            response=f"ERROR: {str(e)}",
            validated=False
        )
        db.add(log)
        db.commit()
        raise


def generate_proposal(client_type: str, budget: float, sustainability_priority: str, products: list, db: Session) -> dict:
    """
    Generate AI-powered B2B proposal with intelligent product recommendations.
    
    Uses OpenAI to analyze budget, sustainability priority, and available products
    to create an optimized product mix with impact positioning.
    
    Args:
        client_type: Type of client (e.g., "retailer", "corporate", "nonprofit")
        budget: Total budget available for proposal
        sustainability_priority: Level of sustainability focus (low, medium, high)
        products: List of Product model instances
        db: SQLAlchemy session for logging
        
    Returns:
        Dict with recommended_products, total_cost, budget_remaining, impact_positioning_summary
    """
    
    # Format product data for AI analysis
    product_list = "\n".join([
        f"- ID: {p.id}, Name: {p.name}, Price: ${p.base_price}, "
        f"Filters: {', '.join(p.sustainability_filters or [])}"
        for p in products[:20]  # Limit to 20 products for token efficiency
    ])
    
    prompt = f"""You are an AI system for sustainable B2B commerce proposals.

Generate an optimal product recommendation mix based on:
- Client Type: {client_type}
- Budget: ${budget}
- Sustainability Priority: {sustainability_priority}

AVAILABLE PRODUCTS:
{product_list}

Return ONLY valid JSON (no markdown):
{{
    "recommendations": [
        {{"product_id": <id>, "quantity": <qty>, "reasoning": "why this product"}}
    ],
    "impact_positioning": "2-3 sentences about sustainability impact",
    "business_rationale": "why this mix matches client needs"
}}

Focus on:
1. Budget optimization (use 85-95% of budget)
2. Sustainability match with client priority
3. Product diversity and complementarity
4. ROI potential for client resale

Return valid JSON only."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a B2B sustainable commerce expert. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        ai_output = response.choices[0].message.content.strip()
        ai_response = json.loads(ai_output)
        
        # Build recommendations with pricing
        recommendations = []
        total_cost = 0
        
        for rec in ai_response.get("recommendations", []):
            product = next((p for p in products if p.id == rec.get("product_id")), None)
            if product:
                quantity = rec.get("quantity", 1)
                unit_price = product.base_price
                cost = quantity * unit_price
                total_cost += cost
                
                recommendations.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": quantity,
                    "unit_price": float(unit_price),
                    "total_price": float(cost),
                    "sustainability_filters": product.sustainability_filters or []
                })
        
        # Log the proposal generation
        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=json.dumps({"recommendations": len(recommendations), "total_cost": total_cost}),
            validated=True
        )
        db.add(log)
        db.commit()
        
        return {
            "recommended_products": recommendations,
            "total_cost": float(total_cost),
            "budget_remaining": float(budget - total_cost),
            "impact_positioning_summary": ai_response.get("impact_positioning", ""),
            "business_rationale": ai_response.get("business_rationale", "")
        }
        
    except Exception as e:
        logger.error(f"Error in proposal generation: {str(e)}")
        log = AILog(
            module_name="proposal_generator",
            prompt=prompt,
            response=f"ERROR: {str(e)}",
            validated=False
        )
        db.add(log)
        db.commit()
        raise





def generate_category_tags(product_data, db: Session):

    prompt = f"""
Classify the product and generate SEO tags.

Product:
Name: {product_data['name']}
Description: {product_data['description']}
Material: {product_data['material']}
Price: {product_data['base_price']}

Return JSON with:
primary_category
sub_category
seo_tags
sustainability_filters
"""

    # Mock AI output (since API quota issue)
    ai_response = {
        "primary_category": "Personal Care",
        "sub_category": "Eco-friendly Oral Care",
        "seo_tags": [
            "bamboo toothbrush",
            "eco toothbrush",
            "biodegradable toothbrush",
            "plastic-free toothbrush",
            "sustainable oral care"
        ],
        "sustainability_filters": [
            "plastic-free",
            "biodegradable",
            "vegan"
        ]
    }

    # Save AI log
    log = AILog(
        module_name="category_generator",
        prompt=prompt,
        response=str(ai_response),
        validated=True
    )

    db.add(log)
    db.commit()

    return ai_response









# def generate_category_tags(product_data):

#     prompt = f"""
# You are an AI system for sustainable commerce.

# Classify the product and generate SEO tags.

# Allowed sustainability filters:
# plastic-free, compostable, vegan, recycled, biodegradable, locally-sourced

# Return ONLY valid JSON in this format:

# {{
#  "primary_category": "",
#  "sub_category": "",
#  "seo_tags": [],
#  "sustainability_filters": []
# }}

# Product information:
# Name: {product_data['name']}
# Description: {product_data['description']}
# Material: {product_data['material']}
# Price: {product_data['base_price']}
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You generate structured JSON outputs only."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.2
#     )

#     ai_output = response.choices[0].message.content

#     return json.loads(ai_output)