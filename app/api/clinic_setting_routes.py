from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import (
    get_current_user,
    admin_required
)

from app.schemas.clinic_setting import (
    ClinicSettingResponse,
    ClinicSettingUpdate
)

from app.services.clinic_setting_service import (
    ClinicSettingService
)

router = APIRouter(
    prefix="/settings",
    tags=["Clinic Settings"]
)


@router.get(
    "/",
    response_model=ClinicSettingResponse
)
def get_settings(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return ClinicSettingService.get(db)


@router.put(
    "/",
    response_model=ClinicSettingResponse
)
def update_settings(
    data: ClinicSettingUpdate,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):

    return ClinicSettingService.update(
        db,
        data
    )