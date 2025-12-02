from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.api.v1.security.jwt_handler import decode_access_token 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("user_id")    
        role: str = payload.get("role")   
        if user_id is None or role is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return payload  
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")  




