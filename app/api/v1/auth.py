from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterRequest, RegisterResponse,LoginRequest,TokenResponse
from app.api.deps import get_database
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_database)
    ):
    return AuthService.register(db,payload)

@router.post("/login",response_model = TokenResponse)
def login(
    payload : LoginRequest,
    db: Session = Depends(get_database)
    ):
# Sekarang result berisi {'token': '...', 'user': <UserObject>}
    result = AuthService.login(db=db, payload=payload)
    
    return {
        'access_token': result['token'],
        'token_type': "bearer",
        'user': {
            'id': result['user'].id,
            'name': result['user'].name,
            'role': result['user'].role
        }
    }