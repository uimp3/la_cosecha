from app.schemas.categoria_schema import CategoriaCrear

categorias = []
contador_id = 1


def listar_categorias():
    return categorias


def crear_categoria(datos: CategoriaCrear):
    global contador_id
    nueva = {"id": contador_id, "nombre": datos.nombre}
    categorias.append(nueva)
    contador_id += 1
    return nueva