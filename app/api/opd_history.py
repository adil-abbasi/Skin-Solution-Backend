from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.opd_history import OPDHistoryResponse
from app.services.opd_history_service import OPDHistoryService


router = APIRouter(
    prefix="/opd",
    tags=["OPD History"],
)


@router.get(
    "/history",
    response_model=OPDHistoryResponse,
)
def get_opd_history(

    period: str = Query(
        default="today",
        description="today, yesterday, week, month, custom",
    ),

    search: str | None = Query(
        default=None,
    ),

    doctor_id: int | None = Query(
        default=None,
    ),

    status: str | None = Query(
        default=None,
    ),

    start_date: date | None = Query(
        default=None,
    ),

    end_date: date | None = Query(
        default=None,
    ),

    page: int = Query(
        default=1,
        ge=1,
    ),

    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),

    db: Session = Depends(get_db),

):

    return OPDHistoryService.get_history(

        db=db,

        period=period,

        search=search,

        doctor_id=doctor_id,

        status=status,

        start_date=start_date,

        end_date=end_date,

        page=page,

        page_size=page_size,

    )