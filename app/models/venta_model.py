from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Venta(Base):
    __tablename__ = "ventas"
    __table_args__ = (
        CheckConstraint("total > 0", name="ck_ventas_total_positivo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    total: Mapped[int]
    vendedor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)

    vendedor: Mapped["Usuario"] = relationship()
    detalles: Mapped[list["DetalleVenta"]] = relationship(back_populates="venta", cascade="all, delete-orphan")

    @property
    def vendedor_nombre(self) -> str:
        return self.vendedor.nombre