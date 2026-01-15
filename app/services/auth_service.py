from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest,LoginRequest
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.core.security import hash_password ,verify_password, create_access_token

class AuthService:
    @staticmethod
    def register(db: Session, payload : RegisterRequest):

        # cek apa ada kesamaan email dengan yang di database
        if UserRepository.get_user_by_email(db,payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Email already Registered"
            )

        # jika match
        # userRole ='user'
        # if(payload.role == 'admin'):
        #     userRole= 'admin'

        user = User(
            name= payload.name,
            email = payload.email,
            password = hash_password(payload.password),
            # set default rule == user            
            role = 'user'
        )
        return UserRepository.create_user(db, user)

        

    def login(db:Session, payload : LoginRequest):
        user = UserRepository.get_user_by_email(db,payload.email)

        if not user:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid credentials"
            )

        if not verify_password(payload.password,user.password):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail= "Invalid credentials"
            )

        token = create_access_token({
            'sub': str(user.id),
            'email': user.email,
            'role':user.role,
        })
        return {
            "token": token,
            "user": user
        }

    # TODO: buat refresh token !!
