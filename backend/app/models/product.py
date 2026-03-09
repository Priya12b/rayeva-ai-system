from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    material = Column(String)
    base_price = Column(Float)

    ai_primary_category = Column(String)
    ai_sub_category = Column(String)

    seo_tags = Column(JSON)
    sustainability_filters = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)