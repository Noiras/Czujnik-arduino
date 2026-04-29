from pydantic import BaseModel, Field
from typing import Optional


class Struct(BaseModel):
    temperatura: float
    cisnienie: float
    wilgotnosc: int = Field(ge=0, le=100)


class StructUpdate(BaseModel):
    temperatura: Optional[float] = None
    cisnienie: Optional[float] = None
    wilgotnosc: Optional[int] = Field(ge=0, le=100, default=None)
    data_pomiaru: Optional[str] = None
