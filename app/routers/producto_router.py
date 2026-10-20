from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.config.database import SesionDB
from app.schemas.importacion_schema import ResultadoImportacion
from app.schemas.producto_schema import ProductoCrear, ProductoRespuesta
from app.seguridad.dependencias import exigir_admin, obtener_usuario_actual
from app.services import categoria_service, importacion_service, producto_service

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
    return producto_service.crear_producto(db, datos)


@router.post(
    "/importar",
    response_model=ResultadoImportacion,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_admin)],
    summary="Cargar el inventario desde Excel",
    responses={422: {"description": "El archivo no es válido o tiene filas con errores. No se guarda nada"}},
)
def importar(archivo: UploadFile, db: SesionDB):
    """
    Recibe un `.xlsx` con las columnas **nombre, precio, stock, categoria** en la primera fila.
    Valida todas las filas antes de guardar: o entran todas, o no entra ninguna.
    """
    contenido = archivo.file.read()
    return importacion_service.importar_inventario(db, archivo.filename or "", contenido)


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
    return producto_service.actualizar_producto(db, producto, datos)


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(exigir_admin)],
)
def eliminar(producto_id: int, db: SesionDB):
    producto = producto_service.buscar_producto(db, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto_service.tiene_ventas(db, producto_id):
        raise HTTPException(status_code=409, detail="No se puede eliminar un producto que ya tiene ventas")
    producto_service.eliminar_producto(db, producto)