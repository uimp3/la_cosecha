from pydantic import BaseModel, ConfigDict, Field


class FilaInventario(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=2, max_length=80)
    precio: int = Field(gt=0)
    stock: int = Field(ge=0)
    categoria: str = Field(min_length=2, max_length=50)


class ResultadoImportacion(BaseModel):
    productos_creados: int
    categorias_creadas: list[str]