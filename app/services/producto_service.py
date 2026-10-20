from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.detalle_venta_model import DetalleVenta
from app.models.producto_model import Producto
from app.schemas.producto_schema import ProductoCrear


def listar_productos(db: Session):
    return db.scalars(select(Producto).order_by(Producto.id)).all()


def buscar_producto(db: Session, producto_id: int):
    return db.get(Producto, producto_id)


def buscar_por_nombre(db: Session, nombre: str):
    return db.scalar(select(Producto).where(Producto.nombre == nombre))


def crear_producto(db: Session, datos: ProductoCrear):
    nuevo = Producto(
        nombre=datos.nombre,
        precio=datos.precio,
        stock=datos.stock,
        categoria_id=datos.categoria_id,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def actualizar_producto(db: Session, producto: Producto, datos: ProductoCrear):
    producto.nombre = datos.nombre
    producto.precio = datos.precio
    producto.stock = datos.stock
    producto.categoria_id = datos.categoria_id
    db.commit()
    db.refresh(producto)
    return producto


def eliminar_producto(db: Session, producto: Producto):
    db.delete(producto)
    db.commit()


def tiene_ventas(db: Session, producto_id: int) -> bool:
    return db.scalar(select(DetalleVenta.id).where(DetalleVenta.producto_id == producto_id).limit(1)) is not None