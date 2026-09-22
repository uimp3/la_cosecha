from fastapi import APIRouter, status
from app.schemas.producto_schema import ProductoCrear, ProductoRespuesta
from app.services import producto_service

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=list[ProductoRespuesta])
def listar():
    return producto_service.listar_productos()

@router.post("/", response_model=ProductoRespuesta, status_code=status.HTTP_201_CREATED)
def crear(datos: ProductoCrear):
    return producto_service.crear_productos(datos)

@router.get("/{producto_id}", response_model=ProductoRespuesta)
def buscar(producto_id: int):
    return producto_service.buscar_producto(producto_id)

@router.put("/{producto_id}", response_model=ProductoRespuesta)
def actualizar(producto_id: int, datos: ProductoCrear):
    return producto_service.actualizar_producto(producto_id, datos)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(producto_id: int):
    return producto_service.eliminar_producto(producto_id)