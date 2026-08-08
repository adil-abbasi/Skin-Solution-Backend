import io
import pandas as pd
from datetime import date

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.opd_history import OPDHistoryResponse
from app.services.opd_history_service import OPDHistoryService

router = APIRouter(
    prefix="/opd",
    tags=["OPD History"],
)

# ---------------------------------------------------
# GET: Standard OPD History (Paginated)
# ---------------------------------------------------
@router.get(
    "/history",
    response_model=OPDHistoryResponse,
)
def get_opd_history(
    period: str = Query(
        default="today",
        description="today, yesterday, week, month, custom",
    ),
    search: str | None = Query(default=None),
    doctor_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
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


# ---------------------------------------------------
# GET: Export OPD History to Excel
# ---------------------------------------------------
@router.get("/history/export")
def export_opd_history(
    period: str = Query(default="today"),
    search: str | None = Query(default=None),
    doctor_id: int | None = Query(default=None),
    status: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
):
    # 1. Fetch data using your existing service
    # Setting page_size to a very high number to get all records for export (e.g., 10,000)
    history_data = OPDHistoryService.get_history(
        db=db,
        period=period,
        search=search,
        doctor_id=doctor_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        page=1,
        page_size=10000, 
    )

    # 2. Format data for Excel safely using getattr() to prevent AttributeErrors
    export_list = []
    
    for record in history_data.records:
        export_list.append({
            # Fallback checks: if visit_date is missing, it checks created_at, then defaults to "N/A"
            "Date": str(getattr(record, "visit_date", getattr(record, "created_at", "N/A"))),
            "Patient Name": getattr(record, "patient_name", "N/A"),
            "Patient Code": getattr(record, "patient_code", "-"), 
            "Phone": getattr(record, "patient_phone", getattr(record, "phone", "N/A")),
            "Doctor": getattr(record, "doctor_name", getattr(record, "doctor", "N/A")),
            "Status": getattr(record, "status", "N/A"),
            "Fee / Revenue": getattr(record, "fee", getattr(record, "amount", 0))
        })

    # 3. Create DataFrame and convert to Excel in memory
    df = pd.DataFrame(export_list)
    buffer = io.BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='OPD History')
    
    buffer.seek(0)

    # 4. Return as a downloadable file
    headers = {
        'Content-Disposition': 'attachment; filename="OPD_History_Export.xlsx"'
    }
    
    return Response(
        content=buffer.getvalue(), 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers
    )