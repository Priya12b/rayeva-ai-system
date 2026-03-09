from pydantic import BaseModel
from typing import List


class CategoryRequest(BaseModel):
    name: str
    description: str
    material: str
    base_price: float


class CategoryResponse(BaseModel):
    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]