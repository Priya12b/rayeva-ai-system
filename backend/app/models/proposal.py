from sqlalchemy import Column, Integer, String, JSON, DateTime, Float
from datetime import datetime
from app.database import Base

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)

    client_type = Column(String)
    budget = Column(Float)

    proposal_json = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)

