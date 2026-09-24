from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserRegister, UserUpdate


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserRegister):
    pass  


def update_user(db: Session, user_id: int, user: UserUpdate, is_admin: bool = False):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user.model_dump(exclude_unset=True)
    
    if "role" in update_data and not is_admin:
        update_data.pop("role")
    
    for key, value in update_data.items():
        if key == "password" and value:
            from app.services.auth_service import hash_password
            setattr(db_user, "password_hash", hash_password(value))
        else:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return True