from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from app.models.product_model import Product
from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate, OrderItemCreate


def get_orders(db: Session):
    return db.query(Order).all()


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_detail(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    return order


def create_order(db: Session, user_id: int, order: OrderCreate):
    # Verificar que el usuario exista
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return "user_not_found"

    total = 0.0
    order_items = []

    # Verificar cada producto y stock
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            return "product_not_found"
        if product.stock < item.quantity:
            return "insufficient_stock"
        
        subtotal = product.price * item.quantity
        total += subtotal
        
        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price
        })

    # Crear el pedido
    db_order = Order(user_id=user_id, status="pendiente")
    db.add(db_order)
    db.flush()  # Para obtener el ID del pedido

    # Crear OrderItems y descontar stock
    for item_data in order_items:
        product = item_data["product"]
        quantity = item_data["quantity"]
        price = item_data["price"]
        
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=product.id,
            quantity=quantity,
            price=price
        )
        db.add(db_item)
        
        # Descontar stock
        product.stock -= quantity

    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_status(db: Session, order_id: int, status: str):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return True