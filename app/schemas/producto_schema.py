from pydantic import BaseModel, Field

class ProductoCrear(BaseModel):

    nombre: str = Field(min_length=2, max_length=80)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    categoria_id: int = Field(gt=0)

class ProductoRespuesta(BaseModel):

    id: int
    nombre: str
    precio: float
    stock: int
    categoria_id: int