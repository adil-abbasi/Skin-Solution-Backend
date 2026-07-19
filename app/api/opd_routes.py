from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.dependencies.auth import get_current_user

from app.schemas.opd import (
    TodayQueueResponse,
    TokenSlipResponse
)

from app.schemas.opd_visit import (
    OPDVisitCreate,
    OPDVisitResponse
)

from app.schemas.queue import (
    CancelVisitRequest,
    MessageResponse
)

from app.services.opd_service import OPDService


router = APIRouter(
    prefix="/opd",
    tags=["OPD"]
)


@router.put(
    "/{visit_id}/complete",
    response_model=MessageResponse
)
def complete_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ok = OPDService.complete_visit(
        db,
        visit_id
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return {
        "message": "Visit completed successfully"
    }


@router.put(
    "/{visit_id}/cancel",
    response_model=MessageResponse
)
def cancel_visit(
    visit_id: int,
    data: CancelVisitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ok = OPDService.cancel_visit(
        db,
        visit_id,
        data.reason
    )

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return {
        "message": "Visit cancelled successfully"
    }


@router.get(
    "/today",
    response_model=list[TodayQueueResponse]
)
def today_queue(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return OPDService.today_queue(db)


@router.post(
    "/generate-token",
    response_model=OPDVisitResponse
)
def generate_token(
    opd_data: OPDVisitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    visit, error = OPDService.generate_token(
        db,
        opd_data
    )

    if error:
        raise HTTPException(
            status_code=404,
            detail=error
        )

    return visit


@router.get(
    "/token/{visit_id}",
    response_model=TokenSlipResponse
)
def print_token(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    slip = OPDService.get_token_slip(
        db,
        visit_id
    )

    if not slip:
        raise HTTPException(
            status_code=404,
            detail="Token not found"
        )

    return slip