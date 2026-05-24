import re

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=6, max_length=72)
    confirm_password: str
    
    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v):
        pattern = r"^[A-Za-zÀ-ỹ\s]+$"
        if not re.match(pattern, v):
            raise ValueError("Name can only contain letters and spaces")
        return v
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        v = v.strip().lower()
        
        pattern = r"^[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 8 characters")
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def check_password_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("email")
    @classmethod
    def normalize(cls, v):
        return v.strip().lower()


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
