from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.emergency_alert import EmergencyAlert
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency_alert import EmergencyAlertCreate
from app.services.email_service import send_email

from app.websocket.manager import manager
import asyncio

router = APIRouter(
    prefix="/alerts",
    tags=["Emergency Alerts"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/trigger")
def trigger_alert(
    alert: EmergencyAlertCreate,
    db: Session = Depends(get_db)
):

    # TEMP USER (replace later with auth system)
    user_id = 2

    # 1. Save alert to database
    new_alert = EmergencyAlert(
        user_id=user_id,
        latitude=alert.latitude,
        longitude=alert.longitude,
        message=alert.message
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    # 2. Fetch emergency contacts
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == user_id
    ).all()

    # 3. Send email alerts
    for contact in contacts:

        body = f"""
🚨 EMERGENCY ALERT 🚨

Message:
{alert.message}

Location:
https://maps.google.com/?q={alert.latitude},{alert.longitude}

Please respond immediately.
"""

        try:
            send_email(
                contact.email,
                "Emergency Alert 🚨",
                body
            )
        except Exception as e:
            print("EMAIL ERROR:", str(e))

    # 4. REAL-TIME WEBSOCKET BROADCAST (SAFE VERSION)
    message = f"🚨 EMERGENCY ALERT: {alert.message} | Location: {alert.latitude},{alert.longitude}"

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.broadcast(message))
    except RuntimeError:
        # fallback safe execution
        asyncio.run(manager.broadcast(message))

    return {
        "message": "Emergency alert triggered successfully",
        "contacts_notified": len(contacts)
    }


@router.get("/history")
def get_alert_history(db: Session = Depends(get_db)):

    user_id = 2  # temporary

    alerts = db.query(EmergencyAlert).filter(
        EmergencyAlert.user_id == user_id
    ).all()

    return alerts