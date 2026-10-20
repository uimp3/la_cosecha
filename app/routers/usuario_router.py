from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import SesionDB
from app.schemas.usuario_schema import UsuarioCrear, UsuarioRespuesta
from app.seguridad.dependencias import exigir_admin
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(exigir_admin)])


@router.get("/", response_model=list[UsuarioRespuesta])
def listar(db: SesionDB):
    return usuario_service.listar_usuarios(db)


@router.post("/", response_model=UsuarioRespuesta, status_code=status.HTTP_201_CREATED)
def crear(datos: UsuarioCrear, db: SesionDB):
    if usuario_service.buscar_por_correo(db, datos.correo) is not None:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese correo")
    return usuario_service.crear_usuario(db, datos)