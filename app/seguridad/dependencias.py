from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config.database import SesionDB
from app.models.usuario_model import Usuario
from app.seguridad.tokens import leer_token
from app.services import usuario_service

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(token: Annotated[str, Depends(esquema_oauth2)], db: SesionDB) -> Usuario:
    error_sesion = HTTPException(
        status_code=401,
        detail="Sesión inválida o vencida. Inicia sesión de nuevo",
        headers={"WWW-Authenticate": "Bearer"},
    )
    usuario_id = leer_token(token)
    if usuario_id is None:
        raise error_sesion
    usuario = usuario_service.buscar_usuario(db, usuario_id)
    if usuario is None or not usuario.activo:
        raise error_sesion
    return usuario


UsuarioActual = Annotated[Usuario, Depends(obtener_usuario_actual)]


def exigir_admin(usuario: UsuarioActual) -> Usuario:
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para esta acción",
        )
    return usuario