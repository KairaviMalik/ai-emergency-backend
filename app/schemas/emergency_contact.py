from pydantic import BaseModel
from app.models import emergency_contact

class EmergencyContactCreate(BaseModel):
    name: str
    phone: str
    relationship: str


class EmergencyContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    relationship: str
    email: str

    class Config:
        from_attributes = True