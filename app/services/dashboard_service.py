from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.opd_visit import OPDVisit


class DashboardService:

    @staticmethod
    def get_dashboard(db: Session):

        today = date.today()

        visits = db.query(OPDVisit).filter(
            OPDVisit.visit_date == today
        )

        return {
            "total_patients_today": visits.count(),

            "waiting": visits.filter(
                OPDVisit.status == "Waiting"
            ).count(),

            "completed": visits.filter(
                OPDVisit.status == "Completed"
            ).count(),

            "cancelled": visits.filter(
                OPDVisit.status == "Cancelled"
            ).count(),

            "revenue_today":
                db.query(
                    func.coalesce(
                        func.sum(OPDVisit.consultation_fee),
                        0
                    )
                ).filter(
                    OPDVisit.visit_date == today,
                    OPDVisit.status == "Completed"
                ).scalar()
        }