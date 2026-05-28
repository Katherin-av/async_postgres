import os
import asyncpg
import dotenv
from loguru import logger

# Cargar variables de entorno
dotenv.load_dotenv()

# Variable global del pool
conn_pool = None


async def init_db():
    """
    Inicializa el connection pool y crea la tabla.
    """
    global conn_pool

    try:
        conn_pool = await asyncpg.create_pool(
            dsn=os.getenv("DATABASE_URL"),
            min_size=1,
            max_size=10,
        )

        logger.info("Conexión a PostgreSQL exitosa")

        # Crear tabla si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
            quantity INT NOT NULL CHECK (quantity >= 0),
            description VARCHAR(255)
        );
        """

        async with conn_pool.acquire() as conn:
            await conn.execute(create_table_query)

        logger.info("Tabla products lista")

    except Exception as e:
        logger.error(f"Error al conectar con PostgreSQL: {e}")
        raise


async def close_db():
    """
    Cierra el connection pool.
    """
    global conn_pool

    if conn_pool:
        await conn_pool.close()
        logger.info("Pool cerrado")


async def get_db() -> asyncpg.Pool:
    """
    Devuelve el connection pool.
    """
    global conn_pool

    if conn_pool is None:
        raise ConnectionError(
            "El pool no está inicializado"
        )

    return conn_pool