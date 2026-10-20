from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Rol = Literal["admin", "vendedor"]


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=128)
    rol: Rol


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    rol: Rol
    activo: bool