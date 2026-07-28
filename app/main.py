from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Database
from app.database.database import Base, engine, SessionLocal

# Models (required so SQLAlchemy creates tables)
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.opd_visit import OPDVisit
from app.models.appointment import Appointment
from app.models.settings import Setting
from backend.app.models.clinic_settings import ClinicSetting

# Authentication
from app.dependencies.auth import get_current_user
from app.services.auth_service import AuthService

# Routers
from app.api.auth_routes import router as auth_router
from app.api.doctor_routes import router as doctor_router
from app.api.patient_routes import router as patient_router
from app.api.opd_routes import router as opd_router
from app.api.opd_history import router as opd_history_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.report_routes import router as report_router
from app.api.export_routes import router as export_router
from app.api.settings_routes import router as settings_router
from app.api.clinic_setting_routes import router as clinic_setting_router
from app.api.appointment_routes import router as appointment_router
from app.api.backup_routes import router as backup_router


app = FastAPI(
    title="Clinic Management System API",
    description="SKIN SOLUTIONS Management Backend",
    version="1.0.0",
)

# ---------------------------------------------------
# Create Database
# ---------------------------------------------------

Base.metadata.create_all(bind=engine)

# ---------------------------------------------------
# Create Default Admin
# ---------------------------------------------------

db = SessionLocal()

try:
    AuthService.create_default_admin(db)
finally:
    db.close()

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Public Routes
# ---------------------------------------------------

app.include_router(auth_router)

# ---------------------------------------------------
# Protected Routes
# ---------------------------------------------------

app.include_router(
    doctor_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    patient_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    opd_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    opd_history_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    dashboard_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    report_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    export_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    settings_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    clinic_setting_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    appointment_router,
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    backup_router,
    dependencies=[Depends(get_current_user)]
)

# ---------------------------------------------------
# Root
# ---------------------------------------------------

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