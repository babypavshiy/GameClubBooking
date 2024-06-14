from typing import Optional

from pydantic import BaseModel

class ReviewCreate(BaseModel):
    """
    Schema for creating a new review
    """
    station_id: int
    rating: float
    comment: Optional[str] = None



class ReviewUpdate(BaseModel):
    """
    Schema for updating an existing review
    """
    station_id: int
    rating: float
    comment: Optional[str] = None