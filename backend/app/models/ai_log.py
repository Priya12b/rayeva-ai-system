from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.database import Base

class AILog(Base):
    __tablename__ = "ai_logs"

    id = Column(Integer, primary_key=True, index=True)

    module_name = Column(String)
    prompt = Column(Text)
    response = Column(Text)

    validated = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)