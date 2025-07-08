from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewIn(BaseModel):
	review_id: str
	user_name: Optional[str]
	rating: int
	review_text: Optional[str]
	review_date: Optional[datetime]

class ReviewOut(BaseModel):

    id: int
    review_id: str
    user_name: Optional[str]
    rating: int
    review_text: Optional[str]
    response_text: str
    response_date: datetime

    class Config:
        orm_mode = True
