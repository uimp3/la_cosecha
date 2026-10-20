from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.config.database import SesionDB
from app.schemas.venta_schema import VentaCrear, VentaRespuesta
from app.seguridad.dependencias import UsuarioActual
from app.services import venta_service

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.post(
    "/",
    response_model=VentaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una venta",
    responses={
        404: {"description": "Uno de los productos no existe"},
        409: {"description": "No hay stock suficiente de algún producto"},
    },
)
def registrar(datos: VentaCrear, db: SesionDB, usuario: UsuarioActual):
    """
    Registra la venta a nombre de quien tiene la sesión abierta.

    - El **vendedor** sale del token, nunca del cuerpo.
    - El **total** y los **subtotales** los calcula el backend con los precios guardados.
    - Si una sola línea falla, **no se guarda nada** ni se descuenta stock.
    """
    return venta_service.registrar_venta(db, datos, usuario)


@router.get(
    "/",
    response_model=list[VentaRespuesta],
    summary="Ventas de un día",
)
def listar(
    db: SesionDB,
    usuario: UsuarioActual,
    fecha: Annotated[date | None, Query(description="Día a consultar (AAAA-MM-DD). Si no se envía, es hoy.")] = None,
):
    """
    La administradora ve todas las ventas del día; una vendedora ve solo las suyas.
    """
    dia = fecha or venta_service.hoy()
    vendedor_id = None if usuario.rol == "admin" else usuario.id
    return venta_service.listar_ventas(db, dia, vendedor_id)