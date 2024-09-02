import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException , Depends 
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Dict
from database.model import Order,ProductInDB
from schemas.schemas import OrderCreate

SECRET_KEY = "secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: Dict[str, str], expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str,):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
outh_2_scheme = OAuth2PasswordBearer(tokenUrl = "Login")

def get_current_user(token : str = Depends(outh_2_scheme)):
    # credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED
    # ,detail = "could not validate",headers = {"WWW-Authenticate":"Bearer"})

    return decode_access_token(token)

def create_order(db: Session, user_id: int, order: OrderCreate):
    db_order = Order(user_id=user_id, product_id=order.product_id, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_product(db: Session, product_id: int):
    return db.query(ProductInDB).filter(ProductInDB.product_id == product_id).first()