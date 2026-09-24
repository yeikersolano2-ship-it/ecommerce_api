from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre del producto", examples=["Mouse Logitech"])
    description: Optional[str] = Field(None, description="Descripción del producto", examples=["Mouse inalámbrico"])
    price: float = Field(..., gt=0, description="Precio del producto (debe ser > 0)", examples=[80000])
    stock: int = Field(..., gt=0, description="Stock del producto (debe ser > 0)", examples=[10])
    category_id: int = Field(..., gt=0, description="ID de la categoría", examples=[1])

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Nombre del producto", examples=["Mouse Logitech G"])
    description: Optional[str] = Field(None, description="Descripción del producto", examples=["Mouse inalámbrico gaming"])
    price: Optional[float] = Field(None, gt=0, description="Precio del producto (debe ser > 0)", examples=[85000])
    stock: Optional[int] = Field(None, gt=0, description="Stock del producto (debe ser > 0)", examples=[15])
    category_id: Optional[int] = Field(None, gt=0, description="ID de la categoría", examples=[2])

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v

    @field_validator("description")
    @classmethod
    def description_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Mouse Logitech",
                "description": "Mouse inalámbrico",
                "price": 80000.0,
                "stock": 10,
                "category_id": 1
            }
        }
    }