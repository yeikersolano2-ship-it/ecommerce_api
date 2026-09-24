from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID del producto", examples=[1])
    quantity: int = Field(..., gt=0, description="Cantidad (debe ser > 0)", examples=[2])


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Lista de productos del pedido (mínimo 1)")

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v: List[OrderItemCreate]) -> List[OrderItemCreate]:
        if not v or len(v) == 0:
            raise ValueError("El pedido debe contener al menos un producto")
        return v


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "status": "pendiente",
                "created_at": "2024-01-15T10:30:00"
            }
        }
    }


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    model_config = {
        "from_attributes": True
    }


class OrderDetailResponse(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "status": "pendiente",
                "created_at": "2024-01-15T10:30:00",
                "items": [
                    {"product_id": 1, "quantity": 2, "price": 80000.0},
                    {"product_id": 3, "quantity": 1, "price": 150000.0}
                ]
            }
        }
    }