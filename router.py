from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from middleware import get_current_user, get_db
from models import User as UserDB, Student as StudentDB, Group as GroupDB  # SQLAlchemy modellari
from schema import *         # Pydantic sxemalari

router = APIRouter()



@router.get("/branch/{branch_name}/users", response_model=List[UserCreate])
async def get_branch_users(
    branch_name: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] == "Superadmin":
        return db.query(UserDB).all()
    if current_user["role"] == "Admin" and current_user["branch"] == branch_name:
        return db.query(UserDB).filter(UserDB.branch == branch_name).all()
    if current_user["role"] == "Teacher":
        student_ids = (
            list(map(int, current_user["students"].split(",")))
            if current_user.get("students") else []
        )
        return db.query(UserDB).filter(UserDB.id.in_(student_ids)).all()
    raise HTTPException(status_code=403, detail="Ruxsat berilmagan")




@router.get("/students", response_model=List[Student])
async def get_students(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    return db.query(StudentDB).all()
@router.post("/students", response_model=Student)
async def create_student(
    student: Student,  # Assuming StudentCreate is the Pydantic model for creating a student
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")

    new_student = StudentDB(**student.dict())  # Assuming you have a StudentDB ORM model
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.put("/students/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: Student,  # Assuming StudentUpdate is the Pydantic model for updating a student
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")

    db_student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.dict(exclude_unset=True).items():  # Update only the fields that were provided
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/groups", response_model=List[Group])
async def get_groups(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    return db.query(GroupDB).all()


@router.post("/groups", response_model=Group)
async def create_group(
    group: Group,  # Assuming GroupCreate is the Pydantic model for creating a group
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")

    new_group = GroupDB(**group.dict())  # Assuming you have a GroupDB ORM model
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.put("/groups/{group_id}", response_model=Group)
async def update_group(
    group_id: int,
    group: Group,  # Assuming GroupUpdate is the Pydantic model for updating a group
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user["role"] != "Superadmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")

    db_group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")

    for key, value in group.dict(exclude_unset=True).items():  # Update only the fields that were provided
        setattr(db_group, key, value)

    db.commit()
    db.refresh(db_group)
    return db_group
