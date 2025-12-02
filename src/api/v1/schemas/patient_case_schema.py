from pydantic import BaseModel
from datetime import date
from typing import Literal

class PatientCaseCreate(BaseModel):
    health_center_id: int
    clinician_id: int
    patient_name: str
    patient_dob: date
    summary: str
    status: Literal["open", "closed"]
    created_at: date
    updated_at: date

class PatientCaseUpdate(BaseModel):
    health_center_id: int | None = None
    clinician_id: int | None = None
    patient_name: str | None = None
    patient_dob: date | None = None
    summary: str | None = None
    status: Literal["open", "closed"] | None = None
    created_at: date | None = None
    updated_at: date | None = None

class PatientCaseResponse(BaseModel):
    id: int
    health_center_id: int
    clinician_id: int
    patient_name: str
    patient_dob: date
    summary: str
    status: Literal["open", "closed"]
    created_at: date
    updated_at: date
    class Config:
        from_attributes = True

class FetchPatientCaseByID(BaseModel):
    id: int


class FetchPatientCaseByOptionalFilters(BaseModel):
    health_center_id: int | None = None
    clinician_id: int | None = None
    patient_name: str | None = None
    patient_dob: date | None = None
    summary: str | None = None
    status: Literal["open", "closed"] | None = None
    created_at: date | None = None  
    updated_at: date | None = None


class DeletePatientCase(BaseModel):
    id: int
    

    