from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.user_service import (
    get_users,
    get_user,
    get_user_by_email,
    update_user,
    delete_user
)
from app.schemas.user_schema import UserUpdate, UserResponse
from app.dependencies.auth_dependencies import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

ADMIN_ROLES = ["admin", "administrador"]


@router.get("/", response_model=list[UserResponse])
def list_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ADMIN_ROLES and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para ver este usuario"
        )
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    is_admin = current_user.role in ADMIN_ROLES
    if not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para actualizar este usuario"
        )
    db_user = update_user(db, user_id, user, is_admin=is_admin)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@router.delete("/{user_id}")
def delete_user_endpoint(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    result = delete_user(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado correctamente"}