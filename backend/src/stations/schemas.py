from pydantic import BaseModel


class StationCreate(BaseModel):
    name: str
    type: str
    is_working: bool = True

class StationUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    is_working: bool | None = True
