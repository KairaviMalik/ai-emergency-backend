from pydantic import BaseModel, EmailStr

class EmergencyContactCreate(BaseModel):
    name: str
    phone: str
    relationship: str
    email: EmailStr


class EmergencyContactResponse(BaseModel):
    id: int
    name: str
    phone: str
    relationship: str
    email: str

    class Config:
        from_attributes = True