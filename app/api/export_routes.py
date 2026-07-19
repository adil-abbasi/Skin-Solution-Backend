from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.services.export_service import ExportService


router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


@router.get("/csv")
def export_csv(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    Path("exports").mkdir(exist_ok=True)

    filename = "exports/opd_report.csv"

    ExportService.export_visits(
        db,
        start_date,
        end_date,
        filename
    )

    return FileResponse(
        path=filename,
        media_type="text/csv",
        filename="opd_report.csv"
    )