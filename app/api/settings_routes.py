from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.settings import (
    SettingsResponse,
    SettingsUpdate
)

from app.services.settings_service import (
    SettingsService
)

router = APIRouter(
    prefix="/settings",
    tags=["Settings"]
)


@router.get(
    "/",
    response_model=SettingsResponse
)
def get_settings(
    db: Session = Depends(get_db)
):

    return SettingsService.get_settings(db)


@router.put(
    "/",
    response_model=SettingsResponse
)
def update_settings(
    data: SettingsUpdate,
    db: Session = Depends(get_db)
):

    return SettingsService.update_settings(
        db,
        data
    )