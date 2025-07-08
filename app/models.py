from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ReviewResponse(Base):
    __tablename__ = "review_responses"
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, nullable=False)
    user_name = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    response_text = Column(String, nullable=False)
    review_date = Column(DateTime, nullable=True)
    response_date = Column(DateTime, default=datetime.utcnow)
