from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categoria_model import Categoria
from app.schemas.categoria_schema import CategoriaCrear


def listar_categorias(db: Session):
    return db.scalars(select(Categoria).order_by(Categoria.id)).all()


def buscar_categoria(db: Session, categoria_id: int):
    return db.get(Categoria, categoria_id)


def buscar_por_nombre(db: Session, nombre: str):
    return db.scalar(select(Categoria).where(Categoria.nombre == nombre))


def crear_categoria(db: Session, datos: CategoriaCrear):
    nueva = Categoria(nombre=datos.nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def actualizar_categoria(db: Session, categoria: Categoria, datos: CategoriaCrear):
    categoria.nombre = datos.nombre
    db.commit()
    db.refresh(categoria)
    return categoria


def eliminar_categoria(db: Session, categoria: Categoria):
    db.delete(categoria)
    db.commit()