from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint("rol IN ('admin', 'vendedor')", name="ck_usuarios_rol_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60))
    correo: Mapped[str] = mapped_column(String(120), unique=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(20))
    activo: Mapped[bool] = mapped_column(default=True)