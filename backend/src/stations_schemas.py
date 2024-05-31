from pydantic import BaseModel


class StationCreate(BaseModel):
    name: str
    is_working: bool = True

class StationUpdate(BaseModel):
    name: str | None = None
    is_working: bool | None = True
