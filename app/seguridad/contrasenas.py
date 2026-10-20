from pwdlib import PasswordHash

hasheador = PasswordHash.recommended()


def hashear(contrasena: str) -> str:
    return hasheador.hash(contrasena)


def verificar(contrasena: str, contrasena_hash: str) -> bool:
    return hasheador.verify(contrasena, contrasena_hash)