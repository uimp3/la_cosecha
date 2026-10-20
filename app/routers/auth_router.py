from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.config.database import SesionDB
from app.schemas.auth_schema import Token
from app.schemas.usuario_schema import UsuarioRespuesta
from app.seguridad.dependencias import UsuarioActual
from app.seguridad.tokens import crear_token
from app.services import usuario_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(formulario: Annotated[OAuth2PasswordRequestForm, Depends()], db: SesionDB):
    usuario = usuario_service.autenticar(db, formulario.username, formulario.password)
    if usuario is None or not usuario.activo:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=crear_token(usuario.id), token_type="bearer")


@router.get("/yo", response_model=UsuarioRespuesta)
def yo(usuario: UsuarioActual):
    return usuario