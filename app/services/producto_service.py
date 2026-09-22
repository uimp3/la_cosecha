from app.schemas.producto_schema import ProductoCrear

productos = []
contador_id = 1

def listar_productos():
    return productos;

def crear_productos(datos: ProductoCrear):
    global contador_id
    nuevo = {
        "id": contador_id,
        "nombre": datos.nombre,
        "precio": datos.precio,
        "stock": datos.stock,
        "categoria_id": datos.categoria_id
    }
    productos.append(nuevo)
    contador_id += 1
    return nuevo

def buscar_producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return None

def actualizar_producto(producto_id: int, datos: ProductoCrear):
    producto = buscar_producto(producto_id)
    if producto:
        producto["nombre"] = datos.nombre
        producto["precio"] = datos.precio
        producto["stock"] = datos.stock
        producto["categoria_id"] = datos.categoria_id
        return producto
    return None

def eliminar_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    if producto:
        productos.remove(producto)
        return True