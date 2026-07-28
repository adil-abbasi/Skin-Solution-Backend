from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.schemas.opd_visit import (
    OPDVisitCreate,
    OPDVisitUpdate,
    OPDVisitResponse,
    TokenPrintResponse,
)

from app.services.opd_service import OPDService
from app.services.opd_history_service import OPDHistoryService


router = APIRouter(
    prefix="/opd",
    tags=["OPD"],
)


# ==================================================
# OPD HISTORY
# IMPORTANT: Keep before /{visit_id}
# ==================================================

@router.get("/history")
def get_opd_history(
    period: str = "today",
    search: str | None = None,
    doctor_id: int | None = None,
    status: str | None = None,
    start_date=None,
    end_date=None,
    page: int = 1,
    page_size: int = 20,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
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


# ==================================================
# CREATE VISIT
# ==================================================

@router.post(
    "/",
    response_model=OPDVisitResponse,
)
def create_visit(
    visit: OPDVisitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.create_visit(
        db,
        visit,
    )


# ==================================================
# CHANGE STATUS
# ==================================================

@router.put("/{visit_id}/status")
def change_status(
    visit_id: int,
    status: str,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.change_status(
        db,
        visit_id,
        status,
    )


# ==================================================
# ALL VISITS
# ==================================================

@router.get(
    "/",
    response_model=list[OPDVisitResponse],
)
def get_all_visits(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.get_all(db)


# ==================================================
# TODAY QUEUE
# ==================================================

@router.get("/today")
def today_visits(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.get_today_visits(db)


# ==================================================
# DASHBOARD
# ==================================================

@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.dashboard(db)


# ==================================================
# SINGLE VISIT
# KEEP BELOW STATIC ROUTES
# ==================================================

@router.get(
    "/{visit_id}",
    response_model=OPDVisitResponse,
)
def get_visit(
    visit_id: int,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.get_visit(
        db,
        visit_id,
    )


# ==================================================
# UPDATE VISIT
# ==================================================

@router.put(
    "/{visit_id}",
    response_model=OPDVisitResponse,
)
def update_visit(
    visit_id: int,

    visit: OPDVisitUpdate,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.update_visit(
        db,
        visit_id,
        visit,
    )


# ==================================================
# CANCEL VISIT
# ==================================================

@router.post("/{visit_id}/cancel")
def cancel_visit(
    visit_id: int,

    reason: str,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    OPDService.cancel_visit(
        db,
        visit_id,
        reason,
    )

    return {
        "message": "Visit cancelled successfully"
    }


# ==================================================
# REPRINT TOKEN
# ==================================================

@router.get(
    "/{visit_id}/reprint",
    response_model=TokenPrintResponse,
)
def reprint_token(
    visit_id: int,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.reprint_token(
        db,
        visit_id,
    )


# ==================================================
# PRINT TOKEN
# ==================================================

@router.get(
    "/{visit_id}/print",
    response_model=TokenPrintResponse,
)
def print_token(
    visit_id: int,

    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return OPDService.get_print_data(
        db,
        visit_id,
    )