from fastapi import APIRouter, Depends, HTTPException, status   
from sqlalchemy.orm import Session

from src.api.v1.deps.db import get_db
from src.api.v1.deps.auth import get_current_user
from src.api.v1.schemas.health_center_schema import HealthCenterCreate, HealthCenterUpdate, HealthCenterResponse, FetchHealthCenterByID, FetchHealthCenterByOptionalFilters, DeleteHealthCenter
from src.models.health_center import HealthCenter 

router = APIRouter(prefix="/health-centers", tags=["Health Centers"])

@router.post("/", response_model=HealthCenterResponse, status_code=status.HTTP_201_CREATED)
def create_health_center(data: HealthCenterCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    hc = HealthCenter(**data.model_dump())
    db.add(hc)
    db.commit()
    db.refresh(hc)
    return hc   

@router.get("/{hc_id}", response_model=HealthCenterResponse)    
def get_health_center_by_id(hc_id:int,db: Session  = Depends(get_db)):
    hc = db.query(HealthCenter).filter(HealthCenter.id == hc_id).first()
    if not hc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health Center not found")
    return hc   

@router.put("/update/{hc_id}", response_model=HealthCenterResponse)
def update_health_center(hc_id:int, data: HealthCenterUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    hc = db.query(HealthCenter).filter(HealthCenter.id == hc_id).first()
    if not hc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health Center not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(hc, key, value)
    db.commit()
    db.refresh(hc)
    return hc

@router.delete("/delete/{hc_id}")
def delete_health_center(hc_id:int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    hc = db.query(HealthCenter).filter(HealthCenter.id == hc_id).first()
    if not hc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health Center not found")
    db.delete(hc)
    db.commit()
    return {"message": "Health Center deleted successfully"}    



    
