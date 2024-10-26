from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import create_access_token, verify_token
from pydantic import BaseModel
from passlib.context import CryptContext

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

def get_password_hash(password):
    return pwd_context.hash(password)

@auth_router.post("/SignUp")
def sign_up(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password,
                    first_name=user.first_name, last_name=user.last_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username}

class Token(BaseModel):
    access_token: str
    token_type: str

@auth_router.post("/SignIn", response_model=Token)
def sign_in(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
