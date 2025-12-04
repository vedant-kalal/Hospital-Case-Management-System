from pydantic import BaseModel,EmailStr
from datetime import date


class ClinicianCreate(BaseModel):
    health_center_id: int   
    name: str
    email: EmailStr
    role: str
    is_active: bool
       

class ClinicianUpdate(BaseModel):
    health_center_id: int | None=None
    name: str | None=None
    email: EmailStr | None=None 
    role: str | None=None
    is_active: bool | None=None

class ClinicianResponse(BaseModel):
    id: int
    health_center_id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    class Config:
        from_attributes = True

class FetchClinicianByID(BaseModel):
    id: int

class FetchClinicianByOptionalFilters(BaseModel):
    health_center_id: int | None=None
    name: str | None=None
    email: EmailStr | None=None
    role: str | None=None
    is_active: bool | None=None

class DeleteClinician(BaseModel):
    id: int


