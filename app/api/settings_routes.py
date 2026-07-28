from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.clinic_settings import ClinicSettings
from app.schemas.settings import (
    SettingsUpdate,
    SettingsResponse
)

from app.dependencies.auth import get_current_user, admin_required


router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)



def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.get(
    "/",
    response_model=SettingsResponse
)
def get_settings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

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
        db.refresh(settings)



    return settings





@router.put(
    "/",
    response_model=SettingsResponse
)
def update_settings(
    data: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):


    settings = db.query(
        ClinicSettings
    ).first()



    if not settings:

        settings = ClinicSettings()

        db.add(settings)



    update_data = data.model_dump(
        exclude_unset=True
    )



    for key, value in update_data.items():

        setattr(
            settings,
            key,
            value
        )



    db.commit()

    db.refresh(settings)



    return settings