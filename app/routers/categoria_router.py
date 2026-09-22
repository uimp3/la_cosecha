from fastapi import APIRouter, status
from app.schemas.categoria_schema import CategoriaCrear, CategoriaRespuesta
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=list[CategoriaRespuesta])
def listar():
    return categoria_service.listar_categorias()


@router.post("/", response_model=CategoriaRespuesta, status_code=status.HTTP_201_CREATED)
def crear(datos: CategoriaCrear):
    return categoria_service.crear_categoria(datos)