from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.emergency_contact import EmergencyContact
from app.schemas.emergency_contact import EmergencyContactCreate

router = APIRouter(
    prefix="/contacts",
    tags=["Emergency Contacts"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_contact(contact: EmergencyContactCreate,
                db: Session = Depends(get_db)):

    new_contact = EmergencyContact(
    user_id=2,
    name=contact.name,
    email=contact.email,
    phone=contact.phone,
    relationship=contact.relationship
)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": "Contact added successfully",
        "contact_id": new_contact.id
    }


@router.get("/")
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(EmergencyContact).all()
    return contacts