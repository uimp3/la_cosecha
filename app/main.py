from fastapi import FastAPI
from app.routers import categoria_router, producto_router

app = FastAPI(title="API de La Cosecha")

app.include_router(categoria_router.router)
app.include_router(producto_router.router)

@app.get("/")
def raiz():
    return {"mensaje": "API de La Cosecha en línea 🌾"}