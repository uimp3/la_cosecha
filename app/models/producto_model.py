from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Producto(Base):
    __tablename__ = "productos"
    __table_args__ = (
        CheckConstraint("precio > 0", name="ck_productos_precio_positivo"),
        CheckConstraint("stock >= 0", name="ck_productos_stock_no_negativo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    precio: Mapped[int]
    stock: Mapped[int]
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))

    categoria: Mapped["Categoria"] = relationship(back_populates="productos")