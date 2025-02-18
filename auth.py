from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from schema import *# Pydantic sxemalari
from models import User as UserModel               # SQLAlchemy modeli
import jwt
from middleware import get_current_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
SECRET_KEY = "mysecretkey"
from models import *
from database import *
from schema import *
auth_router = APIRouter()
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_permission(request: Request, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_role = current_user["role"]
    user_branch = current_user["branch"]


    if user_role == "SuperAdmin":
        return current_user


    branch_param = request.path_params.get("branch_id")
    if branch_param and int(branch_param) != user_branch:
        raise HTTPException(status_code=403, detail="Access denied to this branch")
    
    return current_user


@auth_router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel(
        username=user.username,
        hashed_password=hashed_password, 
        role=user.role,
        branch=user.branch
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = jwt.encode(
        {"username": db_user.username, "role": db_user.role, "branch": db_user.branch},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token}
