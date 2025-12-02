from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.orm import Session  
from src.api.v1.deps.db import get_db
from src.api.v1.deps.auth import get_current_user
from src.api.v1.schemas.case_note_schema import CaseNoteCreate, CaseNoteUpdate, CaseNoteResponse, FetchCaseNoteByID, FetchCaseNoteByOptionalFilters, DeleteCaseNote
from src.models.case_note import CaseNote   

router = APIRouter(prefix="/case-notes", tags=["Case Notes"])

@router.post("/", response_model=CaseNoteResponse, status_code=status.HTTP_201_CREATED)
def create_case_note(data: CaseNoteCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cn = CaseNote(**data.model_dump())
    db.add(cn)
    db.commit()
    db.refresh(cn)
    return cn

@router.get("/{cn_id}", response_model=CaseNoteResponse)
def get_case_note_by_id(cn_id:int,db: Session = Depends(get_db)):
    cn = db.query(CaseNote).filter(CaseNote.id == cn_id).first()
    if not cn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case Note not found")
    return cn

@router.put("/update/{cn_id}", response_model=CaseNoteResponse)
def update_case_note(cn_id:int, data: CaseNoteUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cn = db.query(CaseNote).filter(CaseNote.id == cn_id).first()
    if not cn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case Note not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cn, key, value)
    db.commit()
    db.refresh(cn)
    return cn

@router.delete("/delete/{cn_id}")
def delete_case_note(cn_id:int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    cn = db.query(CaseNote).filter(CaseNote.id == cn_id).first()
    if not cn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case Note not found")
    db.delete(cn)
    db.commit()
    return {"message": "Case Note deleted successfully"}
        
