# Sistema de Gestión de Inventario y Pedidos para E-Commerce

API REST desarrollada con **FastAPI**, **SQLAlchemy**, **SQLite** y **Alembic** para gestión de productos, categorías, usuarios y pedidos con autenticación JWT.

## Características

- **CRUD completo**: Categorías, Productos, Usuarios, Pedidos
- **Autenticación JWT**: Registro, Login, tokens con expiración
- **Roles**: USER (cliente) y ADMIN (administrador)
- **Validaciones**: Pydantic para entrada/salida de datos
- **Migraciones**: Alembic para control de versiones de BD
- **Documentación**: Swagger UI automático en `/docs`
- **Stock automático**: Descuenta inventario al crear pedidos

## Requisitos previos

- Python 3.10+
- Git

## Clonar y ejecutar en otro computador

### 1. Clonar el repositorio
```bash
git clone https://github.com/yeikersolano2-ship-it/ecommerce_api.git
cd ecommerce_api
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv entorno
entorno\Scripts\activate

# Linux/Mac
python3 -m venv entorno
source entorno/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# Editar .env y cambiar SECRET_KEY por una clave segura
# Generar una clave segura:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Ejecutar migraciones (opcional - las tablas se crean automáticamente)
```bash
alembic upgrade head
```

### 6. Iniciar el servidor
```bash
uvicorn app.main:app --reload
```

### 7. Acceder a la API
- **API**: http://127.0.0.1:8000/
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Uso rápido en Swagger

1. Abrir http://127.0.0.1:8000/docs
2. **Registrar usuario**: POST `/auth/register`
3. **Login**: POST `/auth/login` → copiar `access_token`
4. **Authorize**: Pegar el token en el botón "Authorize" (arriba a la derecha)
5. **Probar endpoints protegidos**: GET `/products/`, POST `/orders/`, etc.

## Endpoints principales

### Públicos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar usuario |
| POST | `/auth/login` | Login y obtener token |
| GET | `/categories/` | Listar categorías |
| GET | `/categories/{id}` | Ver categoría |
| GET | `/products/` | Listar productos |
| GET | `/products/{id}` | Ver producto |

### Requieren autenticación (USER/ADMIN)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/orders/` | Crear pedido |
| GET | `/orders/` | Listar mis pedidos |
| GET | `/orders/{id}` | Ver mi pedido |
| GET | `/users/{id}` | Ver mi perfil |
| PUT | `/users/{id}` | Actualizar mi perfil |

### Solo ADMIN
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/categories/` | Crear categoría |
| PUT | `/categories/{id}` | Actualizar categoría |
| DELETE | `/categories/{id}` | Eliminar categoría |
| POST | `/products/` | Crear producto |
| PUT | `/products/{id}` | Actualizar producto |
| DELETE | `/products/{id}` | Eliminar producto |
| GET | `/users/` | Listar todos los usuarios |
| PUT | `/orders/{id}/status` | Cambiar estado de pedido |
| DELETE | `/orders/{id}` | Eliminar pedido |

## Estructura del proyecto
```
ecommerce_api/
├── app/
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── database/
│   │   └── connection.py       # Conexión SQLAlchemy
│   ├── models/                 # Modelos SQLAlchemy
│   │   ├── user_model.py
│   │   ├── category_model.py
│   │   ├── product_model.py
│   │   ├── order_model.py
│   │   └── order_item_model.py
│   ├── schemas/                # Esquemas Pydantic
│   │   ├── user_schema.py
│   │   ├── category_schema.py
│   │   ├── product_schema.py
│   │   └── order_schema.py
│   ├── routes/                 # Endpoints
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── category_routes.py
│   │   ├── product_routes.py
│   │   └── order_routes.py
│   ├── services/               # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── category_service.py
│   │   ├── product_service.py
│   │   └── order_service.py
│   └── dependencies/
│       └── auth_dependencies.py
├── alembic/                    # Migraciones BD
├── .env.example                # Variables de entorno ejemplo
├── .gitignore
└── requirements.txt
```

## Variables de entorno (.env)

```env
SECRET_KEY=tu_clave_secreta_muy_segura
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Comandos útiles

```bash
# Ver migraciones
alembic current
alembic history

# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## Ejemplo de uso

### Registrar usuario
```json
POST /auth/register
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "secret123",
  "phone": "+57 300 123 4567"
}
```

### Login
```json
POST /auth/login
{
  "email": "juan@example.com",
  "password": "secret123"
}
```
Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Crear pedido (requiere token)
```json
POST /orders/
Authorization: Bearer <token>
{
  "items": [
    {"product_id": 1, "quantity": 2}
  ]
}
```

## Tecnologías
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos
- **Alembic** - Migraciones
- **python-jose** - JWT
- **passlib** - Hash de contraseñas
- **Uvicorn** - Servidor ASGI

## Licencia
Proyecto educativo - Aprendiz SENA