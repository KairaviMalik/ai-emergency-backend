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
    try:
        print("===== ALERT RECEIVED =====")
        print(alert)

        user_id = 1

        # Save alert
        new_alert = EmergencyAlert(
            user_id=user_id,
            latitude=alert.latitude,
            longitude=alert.longitude,
            message=alert.message
        )

        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)

        print("ALERT SAVED SUCCESSFULLY")

        # Get contacts
        contacts = db.query(EmergencyContact).filter(
            EmergencyContact.user_id == user_id
        ).all()

        print(f"CONTACTS FOUND: {len(contacts)}")

        # Send emails
        for contact in contacts:
            try:
                body = f"""
🚨 EMERGENCY ALERT 🚨

Message:
{alert.message}

Location:
https://maps.google.com/?q={alert.latitude},{alert.longitude}

Please respond immediately.
"""

                send_email(
                    contact.email,
                    "Emergency Alert 🚨",
                    body
                )

                print(f"EMAIL SENT TO: {contact.email}")

            except Exception as email_error:
                print("EMAIL ERROR:", str(email_error))

        # WebSocket broadcast
        try:
            message = (
                f"🚨 EMERGENCY ALERT: {alert.message} "
                f"| Location: {alert.latitude},{alert.longitude}"
            )

            loop = asyncio.get_running_loop()
            loop.create_task(manager.broadcast(message))

            print("WEBSOCKET BROADCASTED")

        except Exception as ws_error:
            print("WEBSOCKET ERROR:", str(ws_error))

        return {
            "message": "Emergency alert triggered successfully",
            "contacts_notified": len(contacts)
        }

    except Exception as e:
        print("TRIGGER ALERT ERROR:", str(e))
        raise e


@router.get("/history")
def get_alert_history(
    db: Session = Depends(get_db)
):
    user_id = 1

    alerts = db.query(EmergencyAlert).filter(
        EmergencyAlert.user_id == user_id
    ).all()

    return alerts