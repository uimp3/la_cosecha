from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DetalleVentaCrear(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0, le=1000)


class VentaCrear(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"detalles": [{"producto_id": 1, "cantidad": 2}, {"producto_id": 3, "cantidad": 1}]}]
        }
    )

    detalles: list[DetalleVentaCrear] = Field(min_length=1, max_length=50)

    @field_validator("detalles")
    @classmethod
    def sin_productos_repetidos(cls, detalles: list[DetalleVentaCrear]) -> list[DetalleVentaCrear]:
        ids = [detalle.producto_id for detalle in detalles]
        if len(ids) != len(set(ids)):
            raise ValueError("Cada producto va una sola vez: suma las cantidades en una misma línea")
        return detalles


class DetalleVentaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    producto_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario: int
    subtotal: int


class VentaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha: datetime
    total: int
    vendedor_id: int
    vendedor_nombre: str
    detalles: list[DetalleVentaRespuesta]