from pydantic import BaseModel, ConfigDict, Field


class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    precio: int = Field(gt=0)
    stock: int = Field(ge=0)
    categoria_id: int = Field(gt=0)


class ProductoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: int
    stock: int
    categoria_id: int