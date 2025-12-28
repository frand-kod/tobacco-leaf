from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
# jwt provider 
from app.api.deps import get_current_user

# protect router level with token based
router = APIRouter(
    prefix="/user",
     tags=["Users"],
     dependencies = [Depends(get_current_user)]
     )

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/list", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_database)
    # current_user = Depends(get_current_user)
    ):
    return UserService.get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_database)):
    return UserService.get_user(db, user_id)

# maybe tidak dipakai karena single role 
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_database)):
    return UserService.create_user(db, payload)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_database)
):
    return UserService.update_user(db, user_id, payload)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_database)):
    UserService.delete_user(db, user_id)
    return {"message": "User deleted successfully"}