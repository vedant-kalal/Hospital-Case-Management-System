from pydantic import BaseModel
from datetime import date

class CaseNoteCreate(BaseModel):
    case_id: int
    clinician_id: int
    note_text: str
    created_at: date

class CaseNoteUpdate(BaseModel):
    case_id: int | None = None
    clinician_id: int | None = None
    note_text: str | None = None
    created_at: date | None = None

class CaseNoteResponse(BaseModel):
    id: int
    case_id: int
    clinician_id: int
    note_text: str
    created_at: date
    class Config:
        from_attributes = True

class FetchCaseNoteByID(BaseModel):
    id: int

class FetchCaseNoteByOptionalFilters(BaseModel):
    case_id: int | None = None
    clinician_id: int | None = None
    note_text: str | None = None
    created_at: date | None = None

class DeleteCaseNote(BaseModel):
    id: int
