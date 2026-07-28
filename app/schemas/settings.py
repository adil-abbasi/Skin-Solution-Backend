from pydantic import BaseModel
from typing import Optional


class ClinicSettingsBase(BaseModel):

    # Clinic Profile

    clinic_name: str = "My Clinic"

    address: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    logo: Optional[str] = None

    footer_text: Optional[str] = None


    # Print Settings

    show_doctor: bool = True

    show_patient: bool = True


    # OPD Settings

    auto_reset_token: bool = True

    opd_closing_time: str = "22:00"

    token_prefix: str = "T"



class ClinicSettingsCreate(
    ClinicSettingsBase
):
    pass



class ClinicSettingsUpdate(BaseModel):

    clinic_name: Optional[str] = None

    address: Optional[str] = None

    phone: Optional[str] = None

    email: Optional[str] = None

    logo: Optional[str] = None

    footer_text: Optional[str] = None


    show_doctor: Optional[bool] = None

    show_patient: Optional[bool] = None


    auto_reset_token: Optional[bool] = None

    opd_closing_time: Optional[str] = None

    token_prefix: Optional[str] = None



class ClinicSettingsResponse(
    ClinicSettingsBase
):

    id: int


    class Config:
        from_attributes = True



# Compatibility with old routes
# Existing settings_routes.py uses these names

SettingsCreate = ClinicSettingsCreate

SettingsUpdate = ClinicSettingsUpdate

SettingsResponse = ClinicSettingsResponse