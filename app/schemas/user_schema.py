from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre completo del usuario", examples=["Juan Pérez"])
    email: str = Field(..., description="Email del usuario (único)", examples=["juan@example.com"])
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)", examples=["secret123"])
    phone: Optional[str] = Field(None, description="Teléfono del usuario", examples=["+57 300 123 4567"])

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Email inválido")
        return v.lower().strip()

    @field_validator("phone")
    @classmethod
    def phone_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class UserLogin(BaseModel):
    email: str = Field(..., description="Email del usuario", examples=["juan@example.com"])
    password: str = Field(..., description="Contraseña", examples=["secret123"])

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Email inválido")
        return v.lower().strip()


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Nombre completo del usuario", examples=["Juan Pérez"])
    email: Optional[str] = Field(None, description="Email del usuario (único)", examples=["juan@example.com"])
    phone: Optional[str] = Field(None, description="Teléfono del usuario", examples=["+57 300 123 4567"])
    password: Optional[str] = Field(None, min_length=6, description="Contraseña (mínimo 6 caracteres)", examples=["secret123"])

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
                raise ValueError("Email inválido")
            return v.lower().strip()
        return v

    @field_validator("phone")
    @classmethod
    def phone_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            return v if v else None
        return v


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: Optional[str]
    is_active: bool
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "role": "user",
                "phone": "+57 300 123 4567",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00"
            }
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None