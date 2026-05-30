from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)

    message = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())