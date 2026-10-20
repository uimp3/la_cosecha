from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import SesionDB
from app.schemas.categoria_schema import CategoriaCrear, CategoriaRespuesta
from app.seguridad.dependencias import exigir_admin, obtener_usuario_actual
from app.services import categoria_service

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"],
    dependencies=[Depends(obtener_usuario_actual)],
)


@router.get("/", response_model=list[CategoriaRespuesta])
def listar(db: SesionDB):
    return categoria_service.listar_categorias(db)


@router.get("/{categoria_id}", response_model=CategoriaRespuesta)
def obtener(categoria_id: int, db: SesionDB):
    categoria = categoria_service.buscar_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@router.post(
    "/",
    response_model=CategoriaRespuesta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(exigir_admin)],
)
def crear(datos: CategoriaCrear, db: SesionDB):
    if categoria_service.buscar_por_nombre(db, datos.nombre) is not None:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre")
    return categoria_service.crear_categoria(db, datos)


@router.put(
    "/{categoria_id}",
    response_model=CategoriaRespuesta,
    dependencies=[Depends(exigir_admin)],
)
def actualizar(categoria_id: int, datos: CategoriaCrear, db: SesionDB):
    categoria = categoria_service.buscar_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    otra = categoria_service.buscar_por_nombre(db, datos.nombre)
    if otra is not None and otra.id != categoria_id:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre")
    return categoria_service.actualizar_categoria(db, categoria, datos)


@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(exigir_admin)],
)
def eliminar(categoria_id: int, db: SesionDB):
    categoria = categoria_service.buscar_categoria(db, categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoria.productos:
        raise HTTPException(status_code=409, detail="No se puede eliminar una categoría con productos asociados")
    categoria_service.eliminar_categoria(db, categoria)