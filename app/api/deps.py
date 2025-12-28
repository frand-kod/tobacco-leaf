from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.services.user_service import UserService
# nanti di pindah di env
from app.core.security import SECRET_KEY,ALGORITHM
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
auth_scheme = OAuth2PasswordBearer(
    tokenUrl= "/api/v1/auth/login"
)

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token :str = Depends(auth_scheme),
    db:Session= Depends(get_database)
):
    # print("TOKEN get user:", token)
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        user_id : str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail = "Invalid Token"
            )
        # bypass birokrasi
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user 
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = " Invalid or expired token"
        )
