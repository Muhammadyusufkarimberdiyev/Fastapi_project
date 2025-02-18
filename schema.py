
from pydantic import BaseModel, validator
from typing import List, Optional
from pydantic import BaseModel

from pydantic import BaseModel
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    branch: int

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    branch: int

    class Config:
        from_attributes = True
        




class UserLogin(BaseModel):
    username: str
    password: str
class Role(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True

class Branch(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        orm_mode = True

class Group(BaseModel):
    id: Optional[int] = None
    name: str
    branch_id: int

    class Config:
        orm_mode = True

class Student(BaseModel):
    id: Optional[int] = None
    name: str
    group_id: int

    class Config:
        orm_mode = True
