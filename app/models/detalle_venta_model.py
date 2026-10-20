from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class DetalleVenta(Base):
    __tablename__ = "detalles_venta"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_detalles_venta_cantidad_positiva"),
        UniqueConstraint("venta_id", "producto_id", name="uq_detalles_venta_producto"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[int]
    precio_unitario: Mapped[int]
    subtotal: Mapped[int]

    venta: Mapped["Venta"] = relationship(back_populates="detalles")
    producto: Mapped["Producto"] = relationship()

    @property
    def producto_nombre(self) -> str:
        return self.producto.nombre