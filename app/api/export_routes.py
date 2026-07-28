from datetime import date

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.services.export_service import ExportService


router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


# ==================================================
# Export CSV
# ==================================================

@router.get("/csv")
def export_csv(

    start_date: date,
    end_date: date,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user),

):

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



# ==================================================
# Export OPD History Excel
# ==================================================

@router.get("/opd-history")
def export_opd_history(

    period: str = "today",

    search: str | None = None,

    doctor_id: int | None = None,

    status: str | None = None,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user),

):

    excel_file = ExportService.export_opd_history(

        db=db,

        period=period,

        search=search,

        doctor_id=doctor_id,

        status=status,

    )


    return StreamingResponse(

        excel_file,

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={

            "Content-Disposition":
            "attachment; filename=opd_history.xlsx"

        }

    )