from fastapi import APIRouter, HTTPException, Depends,Header,status
from typing import Optional
#from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.model import UserInDB
from database.database import Base,engine,SessionLocal
from schemas.schemas import UserOut,UserCreate
from hashing.hashing import get_password_hash,verify_password
from authentication.authentication  import create_access_token,get_current_user
from sqlalchemy.exc import IntegrityError


router_user = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )


@router_user.post("/signup/", response_model=UserOut,tags = ["Signup"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserInDB).filter(UserInDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(username=user.username,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(user_name=new_user.username)

@router_user.post("/login/",tags = ["Login"])
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserInDB).filter(UserInDB.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

def get_user(db: Session, user_id: int):
    return db.query(UserInDB).filter(UserInDB.id == user_id).first()


def current_user(db: Session = Depends(get_db)):
#     if Authorization is None:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Authorization header missing")
    
#     try:
#         token = Authorization.split(" ")[1]
#     except IndexError:
#         raise HTTPException(status_code=401, detail="Invalid authorization header format")
      
    payload = get_current_user()
    user_id = payload.get("sub")
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="token not specified")
    
    db_user = db.query(UserInDB).filter(UserInDB.id == int(user_id)).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return db_user

@router_user.get("/users/{id}", response_model=UserCreate,tags = ["User"])
def get_users(id :int, db: Session = Depends(get_db), get_current_user : UserCreate = Depends(current_user)):
    db_user = db.query(UserInDB).filter(UserInDB.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserCreate(id = db_user.id , username = db_user.username , password = db_user.hashed_password)

@router_user.delete("/delete_user/{id}", tags=["User"], status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

@router_user.put("/update_user/{id}", tags=["User"], status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserInDB).filter(UserInDB.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user.id = request.id
    user.username = request.username
    user.hashed_password = request.password

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists")
    
    return {"detail": "User updated successfully"}

