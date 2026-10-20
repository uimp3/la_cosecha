from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCrear
from app.seguridad.contrasenas import hashear, verificar

HASH_FALSO = hashear("contrasena-de-relleno")


def listar_usuarios(db: Session):
    return db.scalars(select(Usuario).order_by(Usuario.id)).all()


def buscar_usuario(db: Session, usuario_id: int):
    return db.get(Usuario, usuario_id)


def buscar_por_correo(db: Session, correo: str):
    return db.scalar(select(Usuario).where(Usuario.correo == correo.lower()))


def crear_usuario(db: Session, datos: UsuarioCrear):
    nuevo = Usuario(
        nombre=datos.nombre,
        correo=datos.correo.lower(),
        contrasena_hash=hashear(datos.contrasena),
        rol=datos.rol,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def autenticar(db: Session, correo: str, contrasena: str):
    usuario = buscar_por_correo(db, correo)
    if usuario is None:
        verificar(contrasena, HASH_FALSO)
        return None
    if not verificar(contrasena, usuario.contrasena_hash):
        return None
    return usuario


def crear_admin_inicial(db: Session):
    if db.scalar(select(Usuario.id).limit(1)) is not None:
        return
    admin = Usuario(
        nombre=settings.admin_nombre,
        correo=settings.admin_correo.lower(),
        contrasena_hash=hashear(settings.admin_contrasena),
        rol="admin",
    )
    db.add(admin)
    db.commit()