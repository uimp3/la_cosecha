# 🌾 La Cosecha · API de inventario y ventas
 
Backend de la tienda de Doña Marta en Zipaquirá: inventario, ventas con control de stock, usuarios con roles y carga del inventario desde Excel.
 
Proyecto final del Módulo 4 · Python Backend Developer · [Dev Senior Code](https://devseniorcode.com).
 
## Demo en vivo
 
| Parte | Enlace |
|---|---|
| Backend (API y documentación interactiva) | https://la-cosecha.onrender.com/docs |
| Frontend (tienda) | https://tienda-la-cosecha.onrender.com/ |
 
> **Recomendación:** entra primero al backend. Así la API ya está despierta cuando abras la tienda.
>
> **Ten paciencia la primera vez:** tanto el backend como el frontend están en el plan gratuito de Render, por lo que pueden tardar unos 30 segundos en cargar la primera vez. Después responden con normalidad.
 
## Qué resuelve
 
| Dolor de la tienda | Cómo lo resuelve la API |
|---|---|
| "Vendo algo que ya no tengo" | La venta valida y descuenta el stock en una sola transacción |
| "No sé quién hizo cada venta" | Cada venta guarda a la vendedora, tomada del token |
| "Me cambiaron los precios" | Solo el rol `admin` modifica productos |
| "Sumar me da errores" | El backend calcula subtotales y total con los precios guardados |
| "Todo está en un Excel" | `POST /productos/importar` carga el inventario desde `.xlsx` |
 
## Tecnologías
 
FastAPI · SQLAlchemy 2 · PostgreSQL · Pydantic v2 · JWT (PyJWT) · Argon2 (pwdlib) · openpyxl
 
## Endpoints principales
 
| Método y ruta | Qué hace | Quién |
|---|---|---|
| `POST /auth/login` | Iniciar sesión y recibir el token | Todos |
| `GET /auth/yo` | Ver quién tiene la sesión | Con sesión |
| `GET /productos/` | Listar inventario | Con sesión |
| `POST /productos/` · `PUT` · `DELETE` | Gestionar productos | Admin |
| `POST /productos/importar` | Cargar inventario desde Excel | Admin |
| `GET /categorias/` | Listar categorías | Con sesión |
| `POST /ventas/` | Registrar una venta | Con sesión |
| `GET /ventas/?fecha=AAAA-MM-DD` | Ventas del día (admin: todas · vendedor: las suyas) | Con sesión |
| `GET /usuarios/` · `POST /usuarios/` | Gestionar el equipo | Admin |
 
La documentación interactiva completa está en [`/docs`](https://la-cosecha.onrender.com/docs).
 
## Estructura del repositorio
 
```
la_cosecha/
├── app/               # API (FastAPI)
├── front/             # Frontend de la tienda (sitio estático)
├── .env.example       # Plantilla de variables de entorno
├── .python-version
└── requirements.txt
```
 
## Correr el proyecto en local
 
1. Crear la base de datos `la_cosecha` en PostgreSQL.
2. Crear y activar el entorno virtual:
```bash
# Windows
py -m venv venv
venv\Scripts\activate
 
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
 
pip install -r requirements.txt
```
 
3. Copiar `.env.example` como `.env` y llenar los valores reales.
4. Arrancar:
```bash
fastapi dev app/main.py
```
 
5. Abrir `http://127.0.0.1:8000/docs`.
Para el front: desde la carpeta `front`, ejecutar `py -m http.server 5500` y abrir `http://127.0.0.1:5500/`.
 
## Variables de entorno
 
| Variable | Para qué |
|---|---|
| `DATABASE_URL` | Conexión a PostgreSQL (`postgresql+psycopg://...`) |
| `SECRET_KEY` | Llave para firmar los tokens |
| `ADMIN_NOMBRE`, `ADMIN_CORREO`, `ADMIN_CONTRASENA` | Primera administradora, solo si la tabla de usuarios está vacía |
| `CORS_ORIGINS` | Lista JSON de orígenes del front permitidos |
| `ECHO_SQL` | `true` para ver el SQL en la terminal (solo desarrollo) |
 
## En producción
 
- API: Render (Web Service) · arranque con `fastapi run app/main.py --port $PORT`
- Base de datos: Neon (PostgreSQL)
- Front: Render (Static Site) desde la carpeta `front`
## Créditos
 
Este proyecto parte del proyecto base y del README original de **Ana Alvarado**, Educadora Tech & Desarrolladora Full Stack e instructora de Dev Senior Code ([LinkedIn](https://linkedin.com/in/ana-alvarado-instructora-full-stack)).
 
- Proyecto base y README original: © 2026 Ana Alvarado.
- Desarrollo, adaptación y despliegue: Edwin Danilo Muñoz Tulcan.
