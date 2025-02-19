from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schema, auth
from database import get_db

router = APIRouter()

# Admin qo'shish (faqat SuperAdmin)
@router.post("/admin/")
def add_admin(
    admin: schema.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Only SuperAdmin can add admins")
    new_admin = models.User(
        username=admin.username,
        password_hash=auth.get_password_hash(admin.password),
        branch_id=admin.branch_id,
        role_id=admin.role_id,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

# Branch bo'yicha foydalanuvchilarni olish
@router.get("/branch/{branch_name}/users", response_model=List[schema.UserResponse])
async def get_branch_users(
    branch_name: str,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name == "SuperAdmin":
        return db.query(models.User).all()
    if current_user.role.name == "Admin" and current_user.branch.name == branch_name:
        return db.query(models.User).filter(models.User.branch_id == current_user.branch_id).all()
    raise HTTPException(status_code=403, detail="Ruxsat berilmagan")

# Barcha studentlarni olish (faqat SuperAdmin)
@router.get("/students", response_model=List[schema.Student])
async def get_students(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    return db.query(models.Student).all()

# Student yaratish (faqat SuperAdmin)
@router.post("/students", response_model=schema.Student)
async def create_student(
    student: schema.Student,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# Studentni yangilash (faqat SuperAdmin)
@router.put("/students/{student_id}", response_model=schema.Student)
async def update_student(
    student_id: int,
    student: schema.Student,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student.dict(exclude_unset=True).items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# Barcha guruhlarni olish (faqat SuperAdmin)
@router.get("/groups", response_model=List[schema.Group])
async def get_groups(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    return db.query(models.Group).all()

# Yangi guruh yaratish (faqat SuperAdmin)
@router.post("/groups", response_model=schema.Group)
async def create_group(
    group: schema.Group,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    new_group = models.Group(**group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

# Guruhni yangilash (faqat SuperAdmin)
@router.put("/groups/{group_id}", response_model=schema.Group)
async def update_group(
    group_id: int,
    group: schema.Group,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.name != "SuperAdmin":
        raise HTTPException(status_code=403, detail="Ruxsat berilmagan")
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    for key, value in group.dict(exclude_unset=True).items():
        setattr(db_group, key, value)
    db.commit()
    db.refresh(db_group)
    return db_group
