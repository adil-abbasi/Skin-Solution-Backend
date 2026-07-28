from datetime import date, timedelta
from math import ceil

from sqlalchemy import or_, cast, String
from sqlalchemy.orm import Session, joinedload

from app.models.opd_visit import OPDVisit
from app.models.patient import Patient
from app.models.doctor import Doctor

from app.schemas.opd_history import (
    OPDHistoryRecord,
    OPDHistoryResponse,
    OPDHistorySummary,
    Pagination,
)


class OPDHistoryService:

    @staticmethod
    def get_history(
        db: Session,
        period: str = "today",
        search: str | None = None,
        doctor_id: int | None = None,
        status: str | None = None,
        start_date=None,
        end_date=None,
        page: int = 1,
        page_size: int = 20,
    ):

        query = (
            db.query(OPDVisit)
            .options(
                joinedload(OPDVisit.patient),
                joinedload(OPDVisit.doctor),
            )
            .join(Patient)
            .join(Doctor)
        )

        today = date.today()

        # -------------------------------------------------
        # Date Filters
        # -------------------------------------------------

        if period == "today":

            query = query.filter(
                OPDVisit.visit_date == today
            )

        elif period == "yesterday":

            query = query.filter(
                OPDVisit.visit_date == today - timedelta(days=1)
            )

        elif period == "week":

            query = query.filter(
                OPDVisit.visit_date >= today - timedelta(days=7)
            )

        elif period == "month":

            query = query.filter(
                OPDVisit.visit_date >= today.replace(day=1)
            )

        elif (
            period == "custom"
            and start_date
            and end_date
        ):

            query = query.filter(
                OPDVisit.visit_date.between(
                    start_date,
                    end_date,
                )
            )

        # -------------------------------------------------
        # Search
        # -------------------------------------------------

        if search:

            search = search.strip()

            query = query.filter(

                or_(

                    OPDVisit.visit_number.ilike(
                        f"%{search}%"
                    ),

                    cast(
                        OPDVisit.token_number,
                        String,
                    ).ilike(
                        f"%{search}%"
                    ),

                    Patient.name.ilike(
                        f"%{search}%"
                    ),

                    Doctor.name.ilike(
                        f"%{search}%"
                    ),

                )

            )
                    # -------------------------------------------------
        # Doctor Filter
        # -------------------------------------------------

        if doctor_id:

            query = query.filter(
                OPDVisit.doctor_id == doctor_id
            )

        # -------------------------------------------------
        # Status Filter
        # -------------------------------------------------

        if status:

            query = query.filter(
                OPDVisit.status == status
            )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        total_patients = query.count()

        waiting = query.filter(
            OPDVisit.status == "Waiting"
        ).count()

        completed = query.filter(
            OPDVisit.status == "Completed"
        ).count()

        cancelled = query.filter(
            OPDVisit.status == "Cancelled"
        ).count()

        revenue_rows = (
            query.with_entities(
                OPDVisit.amount_received
            ).all()
        )

        total_revenue = sum(
            row[0] or 0
            for row in revenue_rows
        )

        # -------------------------------------------------
        # Pagination
        # -------------------------------------------------

        total_records = total_patients

        total_pages = (
            ceil(total_records / page_size)
            if total_records > 0
            else 1
        )

        visits = (
            query
            .order_by(
                OPDVisit.visit_date.desc(),
                OPDVisit.token_number.desc(),
            )
            .offset(
                (page - 1) * page_size
            )
            .limit(page_size)
            .all()
        )
                # -------------------------------------------------
        # Prepare Records
        # -------------------------------------------------

        records = []

        for visit in visits:

            records.append(

                OPDHistoryRecord(

                    id=visit.id,

                    token_number=visit.token_number,

                    visit_number=visit.visit_number,

                    patient_name=visit.patient.name,

                    doctor_name=visit.doctor.name,

                    visit_date=visit.visit_date,

                    visit_time=visit.visit_time,

                    consultation_fee=visit.consultation_fee,

                    discount=visit.discount,

                    amount_received=visit.amount_received,

                    payment_method=visit.payment_method,

                    status=visit.status,

                )

            )

        # -------------------------------------------------
        # Return Response
        # -------------------------------------------------

        return OPDHistoryResponse(

            summary=OPDHistorySummary(

                total_patients=total_patients,

                waiting=waiting,

                completed=completed,

                cancelled=cancelled,

                total_revenue=total_revenue,

            ),

            pagination=Pagination(

                page=page,

                page_size=page_size,

                total_records=total_records,

                total_pages=total_pages,

            ),

            records=records,

        )