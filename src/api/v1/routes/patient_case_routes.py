from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.orm import Session  
from src.api.v1.deps.db import get_db
from src.api.v1.deps.auth import get_current_user
from src.api.v1.schemas.patient_case_schema import PatientCaseCreate, PatientCaseUpdate, PatientCaseResponse, FetchPatientCaseByID, FetchPatientCaseByOptionalFilters, DeletePatientCase
from src.models.patient_case import PatientCase

router = APIRouter(prefix="/patient-cases", tags=["Patient Cases"])

@router.post("/", response_model=PatientCaseResponse, status_code=status.HTTP_201_CREATED)
def create_patient_case(data: PatientCaseCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    pc = PatientCase(**data.model_dump())
    db.add(pc)
    db.commit()
    db.refresh(pc)
    return pc

@router.get("/{pc_id}", response_model=PatientCaseResponse)
def get_patient_case_by_id(pc_id:int,db: Session = Depends(get_db)):
    pc = db.query(PatientCase).filter(PatientCase.id == pc_id).first()
    if not pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Case not found")
    return pc

@router.put("/update/{pc_id}", response_model=PatientCaseResponse)
def update_patient_case(pc_id:int, data: PatientCaseUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    pc = db.query(PatientCase).filter(PatientCase.id == pc_id).first()
    if not pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Case not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(pc, key, value)
    db.commit()
    db.refresh(pc)
    return pc

@router.delete("/delete/{pc_id}")
def delete_patient_case(pc_id:int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    pc = db.query(PatientCase).filter(PatientCase.id == pc_id).first()
    if not pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient Case not found")
    db.delete(pc)
    db.commit()
    return {"message": "Patient Case deleted successfully"}
    
