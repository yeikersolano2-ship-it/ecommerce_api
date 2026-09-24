from pydantic import BaseModel, Field, field_validator
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre de la categoría", examples=["Periféricos"])
    description: Optional[str] = Field(None, description="Descripción de la categoría", examples=["Mouse, teclados, audífonos"])

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


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Nombre de la categoría", examples=["Accesorios"])
    description: Optional[str] = Field(None, description="Descripción de la categoría", examples=["Accesorios para computadora"])

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


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Periféricos",
                "description": "Mouse, teclados, audífonos"
            }
        }
    }