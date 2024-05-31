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
    created_at: dt = dt.now()


class ReservationUpdate(BaseModel):
    station_id: int | None = None
    status: int = 0
    user_id: int | None = None
    staff_id: int | None = None
    date: d | None = d.today()
    start_time: dt | None = dt.now()
    end_time: dt | None = dt.now()
    created_at: dt | None = dt.now()