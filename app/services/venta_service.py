from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config.settings import settings
from app.errores import Conflicto, ErrorDeNegocio, NoEncontrado
from app.models.detalle_venta_model import DetalleVenta
from app.models.producto_model import Producto
from app.models.usuario_model import Usuario
from app.models.venta_model import Venta
from app.schemas.venta_schema import VentaCrear

ZONA_TIENDA = timezone(timedelta(hours=settings.zona_horaria_horas))


def hoy() -> date:
    return datetime.now(ZONA_TIENDA).date()


def _consulta_con_detalles():
    return select(Venta).options(
        selectinload(Venta.vendedor),
        selectinload(Venta.detalles).selectinload(DetalleVenta.producto),
    )


def buscar_venta(db: Session, venta_id: int):
    return db.scalar(_consulta_con_detalles().where(Venta.id == venta_id))


def listar_ventas(db: Session, dia: date, vendedor_id: int | None = None):
    inicio = datetime.combine(dia, time.min, tzinfo=ZONA_TIENDA)
    fin = inicio + timedelta(days=1)
    consulta = (
        _consulta_con_detalles()
        .where(Venta.fecha >= inicio, Venta.fecha < fin)
        .order_by(Venta.fecha.desc())
    )
    if vendedor_id is not None:
        consulta = consulta.where(Venta.vendedor_id == vendedor_id)
    return db.scalars(consulta).all()


def registrar_venta(db: Session, datos: VentaCrear, vendedor: Usuario):
    venta = Venta(vendedor_id=vendedor.id)
    total = 0
    try:
        for linea in sorted(datos.detalles, key=lambda detalle: detalle.producto_id):
            producto = db.get(Producto, linea.producto_id, with_for_update=True)
            if producto is None:
                raise NoEncontrado(f"El producto {linea.producto_id} no existe")
            if producto.stock < linea.cantidad:
                raise Conflicto(
                    f"No hay suficiente {producto.nombre}: quedan {producto.stock} y se pidieron {linea.cantidad}"
                )
            producto.stock -= linea.cantidad
            subtotal = producto.precio * linea.cantidad
            venta.detalles.append(
                DetalleVenta(
                    producto_id=producto.id,
                    cantidad=linea.cantidad,
                    precio_unitario=producto.precio,
                    subtotal=subtotal,
                )
            )
            total += subtotal
        venta.total = total
        db.add(venta)
        db.commit()
    except ErrorDeNegocio:
        db.rollback()
        raise
    return buscar_venta(db, venta.id)