from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...v1.schemas.auth_schema import RegisterUser, UserResponse, TokenResponse       
from ...v1.security.jwt_handler import create_access_token 
from ...v1.security.password_hash import hash_password,verify_password
from fastapi.security import OAuth2PasswordRequestForm
from ...v1.deps.db import get_db
from ...v1.deps.auth import get_current_user    
from src.models.user import User    


router = APIRouter(prefix="/auth", tags=["Authentication"]) 

@router.post("/register", response_model=UserResponse)
def register_user(data: RegisterUser, db: Session = Depends(get_db)):
    
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    hashed_password = hash_password(data.password)
    user = User(name=data.name, email=data.email, hashed_password=hashed_password, role=data.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    access_token = create_access_token(data={"user_id": user.id, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

