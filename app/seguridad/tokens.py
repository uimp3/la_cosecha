from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from app.config.settings import settings


def crear_token(usuario_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    contenido = {"sub": str(usuario_id), "exp": expira}
    return jwt.encode(contenido, settings.secret_key, algorithm=settings.algorithm)


def leer_token(token: str) -> int | None:
    try:
        contenido = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )
    except InvalidTokenError:
        return None
    return int(contenido["sub"])