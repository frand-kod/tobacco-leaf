from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repository.user_repository import UserRepository
# hashing
from app.core.security import hash_password

class UserService:

    @staticmethod
    def get_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def create_user(db: Session, payload: UserCreate):
        existing = UserRepository.get_user_by_email(db, payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            name=payload.name,
            email=payload.email,
            password=hash_password(payload.password),
            role=payload.role
        )
        return UserRepository.create_user(db, user)

    @staticmethod
    def update_user(db: Session, user_id: int, payload: UserUpdate):
        user = UserService.get_user(db, user_id)

        if payload.email is not None:
            existing = UserRepository.get_user_by_email(db, payload.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Email already used by another user"
                )
            user.email = payload.email

        if payload.name is not None:
            user.name = payload.name

        if payload.password is not None:
            user.password = hash_password(payload.password)

        if payload.role is not None:
            user.role = payload.role

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserService.get_user(db, user_id)
        UserRepository.delete_user(db, user)
