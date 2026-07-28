from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models.clinic_settings import ClinicSettings
# Database
from app.database.database import Base, engine, SessionLocal
from app.api.user_routes import router as user_router
# Models
from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.opd_visit import OPDVisit
from app.models.clinic_settings import ClinicSettings

# Services
from app.services.auth_service import AuthService

# Dependencies
from app.dependencies.auth import get_current_user

# Routes
from app.api.auth_routes import router as auth_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.doctor_routes import router as doctor_router
from app.api.patient_routes import router as patient_router
from app.api.opd_routes import router as opd_router
from app.api.report_routes import router as report_router
from app.api.export_routes import router as export_router
from app.api.settings_routes import router as settings_router
from app.api import opd_history



@asynccontextmanager
async def lifespan(app: FastAPI):

    # Create database tables
    Base.metadata.create_all(bind=engine)


    db = SessionLocal()

    try:

        # Create default admin
        AuthService.create_default_admin(db)



        # Create default clinic settings
        settings = db.query(
            ClinicSettings
        ).first()


        if not settings:

            settings = ClinicSettings(

                clinic_name="My Clinic",

                show_doctor=True,

                show_patient=True,

                auto_reset_token=True,

                opd_closing_time="22:00",

                token_prefix="T"

            )

            db.add(settings)

            db.commit()



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
# Register Routes
# -----------------------------
app.include_router(user_router)
app.include_router(auth_router)

app.include_router(dashboard_router)

app.include_router(doctor_router)

app.include_router(patient_router)

app.include_router(opd_router)

app.include_router(report_router)

app.include_router(export_router)

app.include_router(settings_router)


# OPD History protected routes
app.include_router(
    opd_history.router,
    dependencies=[Depends(get_current_user)]
)




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

        "message":
        "Clinic Management System Backend Running Successfully"

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