from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.auth import RegisterRequest, RegisterResponse,LoginRequest,TokenResponse
from app.core.security import hash_password
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
    ):
    return AuthService.register(db,payload)

@router.post("/login",response_model = TokenResponse)
def login(
    payload : LoginRequest,
    db: Session = Depends(get_db)
    ):
    token = AuthService.login(
        db=db,
        payload=payload        
    )
    # print(token)
    # balikin access token
    return{
        'access_token' : token,
        'token_type': "bearer"
    }