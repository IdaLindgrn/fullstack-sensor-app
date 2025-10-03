from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    password: str = Field(..., min_length=6, description="User password")


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserOut(BaseModel):
    id: int
    email: str
    username: str


class TokenResponse(BaseModel):
    token: str = Field(..., description="JWT authentication token")
    user: UserOut


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error details")
