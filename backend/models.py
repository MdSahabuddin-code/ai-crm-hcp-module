from sqlalchemy import Column, Integer, String
from db import Base   # ✅ IMPORTANT FIX

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String)
    interaction_type = Column(String)
    sentiment = Column(String)
    date = Column(String)
    time = Column(String)
    topics = Column(String)