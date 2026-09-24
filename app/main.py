from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from app.database.connection import engine, Base
from app.models import User, Category, Product, Order, OrderItem
from app.routes import category_router, product_router, user_router, order_router, auth_router

security = HTTPBearer(auto_error=False)

app = FastAPI(
    title="Sistema de Gestión de Inventario y Pedidos para E-Commerce",
    description="API REST para gestión de productos, categorías y pedidos",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True},
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(category_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"mensaje": "API de Inventario y Pedidos funcionando"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply security to all routes that have dependencies
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if method in ["get", "post", "put", "delete", "patch"]:
                # Skip auth endpoints
                if path not in ["/auth/register", "/auth/login"]:
                    operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi