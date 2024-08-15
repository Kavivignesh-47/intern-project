from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database.model import User
from database.database import Base,engine,SessionLocal
from schemas.schemas import UserOut,UserCreate
from hashing.hashing import get_password_hash,verify_password

app = FastAPI()

Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/signup/", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.get("/users/", response_model=UserOut)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users



