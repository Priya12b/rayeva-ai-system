from pydantic import BaseModel
from typing import List, Optional


class ProposalRequest(BaseModel):
    client_type: str
    budget: float
    sustainability_priority: str


class ProductRecommendation(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    sustainability_filters: List[str] = []


class ProposalResponse(BaseModel):
    recommended_products: List[ProductRecommendation]
    total_cost: float
    budget_remaining: float
    impact_positioning_summary: str
    business_rationale: Optional[str] = None

    