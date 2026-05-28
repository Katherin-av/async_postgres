from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import init_db, close_db
from routes.product_routes import product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la aplicación."""
    # Al iniciar: crear el pool de BD
    await init_db()
    yield
    # Al apagar: cerrar el pool
    await close_db()


# Crear la app FastAPI con el lifespan
app = FastAPI(
    lifespan=lifespan,
    title="Gestor de Inventario FastAPI",
    description="API asíncrona de productos con PostgreSQL",
    version="1.0.0"
)

# Registrar el router de productos
app.include_router(product_router)