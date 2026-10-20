import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("la_cosecha")


class ErrorDeNegocio(Exception):
    codigo_http = 400

    def __init__(self, mensaje: str, errores: list[str] | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.errores = errores or []


class NoEncontrado(ErrorDeNegocio):
    codigo_http = 404


class Conflicto(ErrorDeNegocio):
    codigo_http = 409


class DatosInvalidos(ErrorDeNegocio):
    codigo_http = 422


def registrar_manejadores(app: FastAPI):
    @app.exception_handler(ErrorDeNegocio)
    async def manejar_error_de_negocio(request: Request, error: ErrorDeNegocio):
        contenido = {"detail": error.mensaje}
        if error.errores:
            contenido["errores"] = error.errores
        return JSONResponse(status_code=error.codigo_http, content=contenido)

    @app.exception_handler(IntegrityError)
    async def manejar_error_de_integridad(request: Request, error: IntegrityError):
        logger.warning("Regla de la base de datos incumplida en %s: %s", request.url.path, error.orig)
        return JSONResponse(
            status_code=409,
            content={"detail": "La operación choca con una regla de la base de datos: el dato está repetido o en uso"},
        )