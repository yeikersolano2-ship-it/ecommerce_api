from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.category_service import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category
)
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse
from app.dependencies.auth_dependencies import get_current_user, require_admin

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category_endpoint(
    category: CategoryCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_category = create_category(db, category)
    return db_category


@router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(
    category_id: int,
    category: CategoryUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_category = update_category(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category


@router.delete("/{category_id}")
def delete_category_endpoint(
    category_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    result = delete_category(db, category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if result is False:
        raise HTTPException(status_code=400, detail="No se puede eliminar la categoría")
    return {"mensaje": "Categoría eliminada correctamente"}