from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_patients_today: int

    waiting: int

    completed: int

    cancelled: int

    revenue_today: float

    pending_payment: float