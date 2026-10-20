from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.config.database import SesionDB
from app.schemas.producto_schema import ProductoCrear, ProductoRespuesta
from app.seguridad.dependencias import exigir_admin, obtener_usuario_actual
from app.services import categoria_service, producto_service

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    dependencies=[Depends(obtener_usuario_actual)],
)


@router.get("/", response_model=list[ProductoRespuesta])
def listar(db: SesionDB):
    return producto_service.listar_productos(db)


@router.get("/{producto_id}", response_model=ProductoRespuesta)
def obtener(producto_id: int, db: SesionDB):
    producto = producto_service.buscar_producto(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post(
    "/",
    response_model=ProductoRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_admin)],
)
def crear(datos: ProductoCrear, db: SesionDB):
    if categoria_service.buscar_categoria(db, datos.categoria_id) is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if producto_service.buscar_por_nombre(db, datos.nombre) is not None:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
    try:
        return producto_service.crear_producto(db, datos)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto de integridad al crear el producto") from error


@router.put(
    "/{producto_id}",
    response_model=ProductoRespuesta,
    dependencies=[Depends(exigir_admin)],
)
def actualizar(producto_id: int, datos: ProductoCrear, db: SesionDB):
    producto = producto_service.buscar_producto(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if categoria_service.buscar_categoria(db, datos.categoria_id) is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    otro = producto_service.buscar_por_nombre(db, datos.nombre)
    if otro is not None and otro.id != producto_id:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
    try:
        return producto_service.actualizar_producto(db, producto, datos)
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto de integridad al actualizar el producto") from error


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(exigir_admin)],
)
def eliminar(producto_id: int, db: SesionDB):
    producto = producto_service.buscar_producto(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_service.eliminar_producto(db, producto)