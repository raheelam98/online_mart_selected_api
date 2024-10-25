from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlmodel import select
from datetime import datetime, timedelta, timezone

from app.settings import SECRET_KEY, ADMIN_SECRET_KEY, ALGORITHM
from app.db.db_connector import DB_SESSION
from app.models.auth_admin_model import Admin

### ============================================================================================================= ###

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

### ============================================================================== ###

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/v1")

def create_access_token(subject: str , expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f' to_encode .....  {to_encode}')
    return encoded_jwt

### ============================================================================== ###

def decode_access_token(access_token: str):
    decoded_jwt = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_jwt

### ============================================================================== ###


### ============================================================================== ###
### ============================================================================== ###
### ============================================================================== ### 


def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials")
    
### ============================================================================== ###
 
def admin_required(token: Annotated[str, Depends(oauth2_scheme)], session: DB_SESSION):
    headers = jwt.get_unverified_headers(token)
    admin_secret = headers.get("secret")
    admin_name = headers.get("name")
    admin_kid = headers.get("kid")
    payload = decode_jwt(token)
    admin = session.exec(select(Admin).where(Admin.admin_name == payload.get(
        "admin_name")).where(Admin.admin_email == payload.get("admin_email")).where(Admin.admin_kid == admin_kid)).one_or_none()
   
    print(f'admin : {admin}')
    print(f"Admin Secret : {admin_secret}")
    print(f'payload : {payload}')
    #print(f'token : {token}')

    if not admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not (str(admin_secret) == str(ADMIN_SECRET_KEY)):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return payload

### ============================================================================== ###







