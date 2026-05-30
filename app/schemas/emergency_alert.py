from pydantic import BaseModel


class EmergencyAlertCreate(BaseModel):
    latitude: str
    longitude: str
    message: str