from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel
from datetime import date as d, datetime as dt

class ReservationCreate(BaseModel):
    station_id: int
    status: int = 0
    user_id: int
    staff_id: int
    date: d = d.today()
    start_time: dt = dt.now()
    end_time: dt = dt.now()


class ReservationUpdate(BaseModel):
    station_id: Optional[int] = None
    status: int = 0
    user_id: Optional[int] = None
    staff_id: Optional[int] = None
    date: Optional[d] = d.today()
    start_time: Optional[dt] = dt.now()
    end_time: Optional[dt] = dt.now()