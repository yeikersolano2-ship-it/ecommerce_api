from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.product_service import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product
)
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.dependencies.auth_dependencies import get_current_user, require_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product_endpoint(
    product: ProductCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_product = create_product(db, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_product


@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    db_product = update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if db_product == "category_not_found":
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_product


@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    result = delete_product(db, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}