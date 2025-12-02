from pydantic import BaseModel
from datetime import date


class HealthCenterCreate(BaseModel):
    name: str
    address: str
    is_active: bool
    created_at: date 

class HealthCenterUpdate(BaseModel):
    name: str | None=None
    address: str | None=None 
    is_active: bool | None=None 
    created_at: date | None=None    

class HealthCenterResponse(BaseModel):
    id: int
    name: str
    address: str
    is_active: bool
    created_at: date 
    class Config:
        from_attributes = True

class FetchHealthCenterByID(BaseModel):
    id: int 

class FetchHealthCenterByOptionalFilters(BaseModel):
    name: str | None=None 
    address: str | None=None 
    is_active: bool | None=None 
    created_at: date | None=None 
    
class DeleteHealthCenter(BaseModel):
    id: int 


    

          