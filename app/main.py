from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.config.database import Base, SesionLocal, engine
from app.config.settings import settings
from app.errores import registrar_manejadores
from app.routers import auth_router, categoria_router, producto_router, usuario_router, venta_router
from app.services import usuario_service

DESCRIPCION = """
Sistema de inventario y ventas de **La Cosecha**, la tienda de Doña Marta en Zipaquirá.

**Cómo probarla:** usa `POST /auth/login` o el botón **Authorize** con un correo y contraseña.
Las vendedoras registran ventas; solo la administradora modifica el inventario y los usuarios.
"""

ETIQUETAS = [
    {"name": "Estado", "description": "Comprobar que la API está en línea."},
    {"name": "Autenticación", "description": "Iniciar sesión y saber quién soy."},
    {"name": "Usuarios", "description": "Cuentas del equipo. **Solo admin.**"},
    {"name": "Categorías", "description": "Agrupan los productos. Leer: con sesión · Escribir: admin."},
    {"name": "Productos", "description": "Inventario, precios, stock y carga desde Excel. Escribir: admin."},
    {"name": "Ventas", "description": "Registrar ventas y consultar el historial del día."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SesionLocal() as db:
        usuario_service.crear_admin_inicial(db)
    yield


app = FastAPI(
    title="API de La Cosecha",
    version="1.0.0",
    description=DESCRIPCION,
    openapi_tags=ETIQUETAS,
    lifespan=lifespan,
)

registrar_manejadores(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(usuario_router.router)
app.include_router(categoria_router.router)
app.include_router(producto_router.router)
app.include_router(venta_router.router)


@app.get("/", tags=["Estado"], summary="¿La API está en línea?")
def raiz():
    return {"mensaje": "API de La Cosecha en línea 🌾"}