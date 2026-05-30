from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine

from app.models.user import User
from app.models.emergency_contact import EmergencyContact
from app.models.emergency_alert import EmergencyAlert

from app.routes import auth
from app.routes import emergency_contact
from app.routes import emergency_alert
from app.routes import ai
from app.routes import ws_alerts   # 🔥 WebSocket routes

app = FastAPI(title="AI Emergency Guardian API")

# 🔥 CORS FIX (THIS IS WHAT YOU ARE MISSING)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # in production you will restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# REST ROUTES
app.include_router(auth.router)
app.include_router(emergency_contact.router)
app.include_router(emergency_alert.router)
app.include_router(ai.router)

# WEBSOCKET ROUTE
app.include_router(ws_alerts.router)


@app.get("/")
def root():
    return {"message": "AI Emergency Guardian Backend Running"}