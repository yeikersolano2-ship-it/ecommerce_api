from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.auth_service import decode_token
from app.models.user_model import User


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
    )
    
    if not authorization:
        raise credentials_exception
    
    # Accept both "Bearer <token>" and just "<token>"
    token = authorization
    if authorization.startswith("Bearer "):
        token = authorization[7:]  # Remove "Bearer "
    
    token_data = decode_token(token)
    if token_data is None or token_data.user_id is None:
        raise credentials_exception
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    admin_roles = ["admin", "administrador"]
    if current_user.role not in admin_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de administrador"
        )
    return current_user