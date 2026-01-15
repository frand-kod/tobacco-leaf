from pydantic import BaseModel,EmailStr,Field

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length = 72)
    # role: str | null

class RegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role : str

class LoginRequest(BaseModel):
    email: EmailStr
    password : str

class UserInfo(BaseModel):
    id: int
    name : str
    role: str

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = "bearer"
    user:UserInfo


