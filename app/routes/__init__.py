from app.routes.category_routes import router as category_router
from app.routes.product_routes import router as product_router
from app.routes.user_routes import router as user_router
from app.routes.order_routes import router as order_router
from app.routes.auth_routes import router as auth_router

__all__ = ["category_router", "product_router", "user_router", "order_router", "auth_router"]