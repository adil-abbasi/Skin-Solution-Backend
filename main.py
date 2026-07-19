from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database
from app.database.database import Base, engine, SessionLocal
from app.models.clinic_setting import ClinicSetting
# Models
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.opd_visit import OPDVisit

# Services
from app.services.auth_service import AuthService

# Routes
from app.api.auth_routes import router as auth_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.doctor_routes import router as doctor_router
from app.api.patient_routes import router as patient_router
from app.api.opd_routes import router as opd_router
from app.api.report_routes import router as report_router
from app.api.export_routes import router as export_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Create default admin user
    db = SessionLocal()
    try:
        AuthService.create_default_admin(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="Clinic Management System API",
    description="Offline Clinic Management Backend",
    version="1.0.0",
    lifespan=lifespan
)

# -----------------------------
# Register API Routes
# -----------------------------
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(opd_router)
app.include_router(report_router)
app.include_router(export_router)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Clinic Management System Backend Running Successfully"
    }


# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "OK",
        "database": "Connected"
    }