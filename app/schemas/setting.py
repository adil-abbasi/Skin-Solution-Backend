from pydantic import BaseModel


class SettingsResponse(BaseModel):
    clinic_name: str
    address: str
    phone: str
    email: str
    currency: str
    receipt_footer: str

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    clinic_name: str
    address: str
    phone: str
    email: str
    currency: str
    receipt_footer: str