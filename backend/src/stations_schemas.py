from pydantic import BaseModel


class StationCreate(BaseModel):
    name: str
    is_working: bool = True
