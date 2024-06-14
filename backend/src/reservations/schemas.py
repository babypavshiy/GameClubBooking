from typing import Optional
from pydantic import BaseModel
from datetime import date as d, datetime as dt

class ReservationCreate(BaseModel):
    station_id: int
    status: int = 0
    date: d = d.today()
    start_time: dt = dt.now()


class ReservationUpdate(BaseModel):
    station_id: Optional[int] = None
    status: int = 0
    date: Optional[d] = d.today()
    start_time: Optional[dt] = dt.now()
