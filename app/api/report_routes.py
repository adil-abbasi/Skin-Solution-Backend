from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.services.report_service import ReportService
from app.utils.pdf_generator import generate_report


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/today/pdf")
def today_pdf(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    visits = ReportService.today(db)

    data = [
        [
            "Token",
            "Patient",
            "Doctor",
            "Fee",
            "Status"
        ]
    ]

    for visit in visits:

        data.append([
            visit.token_number,
            visit.patient.name,
            visit.doctor.name,
            visit.consultation_fee,
            visit.status
        ])

    Path("exports").mkdir(exist_ok=True)

    filename = "exports/today_report.pdf"

    generate_report(
        data,
        filename
    )

    return FileResponse(
        path=filename,
        media_type="application/pdf",
        filename="today_report.pdf"
    )