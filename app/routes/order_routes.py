from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.order_service import (
    get_orders,
    get_orders_by_user,
    get_order,
    get_order_detail,
    create_order,
    update_order_status,
    delete_order
)
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderDetailResponse
from app.dependencies.auth_dependencies import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderDetailResponse, status_code=201)
def create_order_endpoint(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = create_order(db, current_user.id, order)
    if result == "user_not_found":
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if result == "product_not_found":
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if result == "insufficient_stock":
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    return get_order_detail(db, result.id)


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ADMIN_ROLES = ["admin", "administrador"]
    if current_user.role in ADMIN_ROLES:
        return get_orders(db)
    return get_orders_by_user(db, current_user.id)


@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_endpoint(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ADMIN_ROLES = ["admin", "administrador"]
    db_order = get_order_detail(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if current_user.role not in ADMIN_ROLES and db_order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permisos para ver este pedido")
    return db_order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status_endpoint(
    order_id: int,
    status: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    valid_statuses = ["pendiente", "confirmado", "enviado", "entregado", "cancelado"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Estado inválido")
    db_order = update_order_status(db, order_id, status)
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_order


@router.delete("/{order_id}")
def delete_order_endpoint(
    order_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    result = delete_order(db, order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado correctamente"}