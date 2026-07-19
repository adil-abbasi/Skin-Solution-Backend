from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.settings_routes import router as settings_router
from app.database.database import engine, Base
from app.models.appointment import Appointment
from app.api.appointment_routes import router as appointment_router
from app.api.backup_routes import router as backup_router
from app.api.clinic_setting_routes import router as clinic_setting_router
# Import Models
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.opd_visit import OPDVisit
from app.models.settings import Setting
# Import Routes
from app.api.doctor_routes import router as doctor_router
from app.api.patient_routes import router as patient_router
from app.api.backup_routes import router as backup_router
from app.api.auth_routes import router as auth_router
from app.database.database import SessionLocal
from app.services.auth_service import AuthService
app = FastAPI(
    title="Clinic Management System API",
    description="Offline Clinic Management Backend",
    version="1.0.0"
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Register Routes
app.include_router(clinic_setting_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(settings_router)
app.include_router(appointment_router)
app.include_router(backup_router)
app.include_router(backup_router)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Clinic Management System Backend Running Successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "database": "Connected"
    }