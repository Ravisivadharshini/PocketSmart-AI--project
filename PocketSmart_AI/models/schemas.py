from typing import Optional
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=4)

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    room_type: str
    items: str = ""
    style: str = "Modern"

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    guests: int = Field(gt=0)
    event_type: str
    venue: str = ""
    preferences: str = ""

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str
    style: str = "Elegant"
    outfit_color: Optional[str] = None
    image_name: Optional[str] = None
