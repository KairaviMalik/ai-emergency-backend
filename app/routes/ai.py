from fastapi import APIRouter
from app.schemas.ai import AnalyzeRequest
import joblib

from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.database import SessionLocal
from app.models.emergency_alert import EmergencyAlert
from app.models.emergency_contact import EmergencyContact

router = APIRouter(
    prefix="/ai",
    tags=["AI Detection"]
)

model = joblib.load("emergency_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze")
def analyze_text(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):

    text_vector = vectorizer.transform([request.text])

    prediction = model.predict(text_vector)[0]

    probability = float(
        model.predict_proba(text_vector)[0][1]
    )

    emergency = bool(prediction)

    response = {
        "text": request.text,
        "emergency": emergency,
        "confidence": round(probability, 2)
    }

    if emergency:

        alert = EmergencyAlert(
            user_id=2,   # temporary
            latitude=request.latitude,
            longitude=request.longitude,
            message=request.text
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        contacts = db.query(
            EmergencyContact
        ).filter(
            EmergencyContact.user_id == 2
        ).all()

        response["alert_created"] = True
        response["alert_id"] = alert.id
        response["contacts_notified"] = len(contacts)

    return response