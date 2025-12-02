from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.orm import Session

from src.api.v1.deps.db import get_db
from src.api.v1.deps.auth import get_current_user
from src.api.v1.schemas.clinician_schema import ClinicianCreate, ClinicianUpdate, ClinicianResponse, FetchClinicianByID, FetchClinicianByOptionalFilters, DeleteClinician
from src.models.clinician import Clinician

router = APIRouter(prefix="/clinicians", tags=["Clinicians"])

@router.post("/", response_model=ClinicianResponse, status_code=status.HTTP_201_CREATED)
def create_clinician(data: ClinicianCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    hc = Clinician(**data.model_dump())
    db.add(hc)
    db.commit()
    db.refresh(hc)
    return hc

@router.get("/{clinician_id}", response_model=ClinicianResponse)
def get_clinician_by_id(clinician_id:int , db:Session = Depends(get_db)):
    clinician = db.query(Clinician).filter(Clinician.id == clinician_id).first()
    if not clinician:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinician not found")
    return clinician

@router.put("/update/{clinician_id}", response_model=ClinicianResponse)
def update_clinician(clinician_id:int, data: ClinicianUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    clinician = db.query(Clinician).filter(Clinician.id == clinician_id).first()
    if not clinician:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinician not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(clinician, key, value)
    db.commit()
    db.refresh(clinician)
    return clinician

@router.delete("/delete/{clinician_id}")
def delete_clinician(clinician_id:int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    clinician = db.query(Clinician).filter(Clinician.id == clinician_id).first()
    if not clinician:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinician not found")
    db.delete(clinician)
    db.commit()
    return {"message": "Clinician deleted successfully"}

