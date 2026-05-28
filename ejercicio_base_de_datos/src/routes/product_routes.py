from fastapi import HTTPException, Body, APIRouter, Depends, Path, Query
from models.product_models import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductStockUpdate,
)
from database.db import get_db
import asyncpg
from loguru import logger

product_router = APIRouter()


@product_router.post("/products", response_model=Product)
async def create_product(
    product: ProductCreate = Body(...),
    db_pool: asyncpg.Pool = Depends(get_db),
) -> Product:
    """
    Crea un nuevo producto.
    """
    query = """
    INSERT INTO products (name, price, quantity, description)
    VALUES ($1, $2, $3, $4)
    RETURNING id, name, price, quantity, description
    """
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(
                query,
                product.name,
                product.price,
                product.quantity,
                product.description,
            )
            if result:
                return Product(**dict(result))
            else:
                logger.error("Error al crear el producto")
                raise HTTPException(
                    status_code=500,
                    detail="Error al crear el producto"
                )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@product_router.get("/products", response_model=list[Product])
async def get_all_products(
    db_pool: asyncpg.Pool = Depends(get_db),
) -> list[Product]:
    """
    Obtiene una lista de todos los productos.
    """
    query = "SELECT id, name, price, quantity, description FROM products"
    try:
        async with db_pool.acquire() as conn:
            results = await conn.fetch(query)
            return [Product(**dict(result)) for result in results]
    except Exception as e:
        logger.error(f"Error al obtener productos: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al recuperar productos"
        )

@product_router.get("/products/{id}", response_model=Product)
async def get_product_by_id(
    id: int = Path(..., ge=1),
    db_pool: asyncpg.Pool = Depends(get_db),
) -> Product:
    """
    Obtiene un producto por su ID.
    """
    query = "SELECT id, name, price, quantity, description FROM products WHERE id = $1"
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(query, id)
            if result:
                return Product(**dict(result))
            else:
                logger.warning(f"Producto con ID {id} no encontrado")
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener producto: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@product_router.put("/products/{id}", response_model=Product)
async def update_product(
    id: int = Path(..., ge=1),
    product: ProductUpdate = Body(...),
    db_pool: asyncpg.Pool = Depends(get_db),
) -> Product:
    """
    Actualiza un producto por su ID.
    Permite actualizaciones parciales.
    """
    query = """
    UPDATE products
    SET name = COALESCE($1, name),
        price = COALESCE($2, price),
        quantity = COALESCE($3, quantity),
        description = COALESCE($4, description)
    WHERE id = $5
    RETURNING id, name, price, quantity, description
    """
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(
                query,
                product.name,
                product.price,
                product.quantity,
                product.description,
                id,
            )
            if result:
                return Product(**dict(result))
            else:
                logger.warning(f"Producto {id} no encontrado")
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@product_router.delete("/products/{id}")
async def delete_product(
    id: int = Path(..., ge=1),
    db_pool: asyncpg.Pool = Depends(get_db)
) -> dict:
    """
    Elimina un producto por su ID.
    """
    query = "DELETE FROM products WHERE id = $1 RETURNING id"
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(query, id)
            if result:
                return {"message": "Producto eliminado exitosamente"}
            else:
                logger.warning(f"Producto {id} no encontrado")
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

@product_router.patch("/products/{id}/stock", response_model=Product)
async def update_product_stock(
    id: int = Path(..., ge=1),
    stock: ProductStockUpdate = Body(...),
    db_pool: asyncpg.Pool = Depends(get_db),
) -> Product:
    """
    Actualiza el stock (cantidad) de un producto.
    """
    query = """
    UPDATE products
    SET quantity = $1
    WHERE id = $2
    RETURNING id, name, price, quantity, description
    """
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(
                query,
                stock.quantity,
                id
            )
            if result:
                return Product(**dict(result))
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Producto no encontrado"
                )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar stock: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar stock"
        )

@product_router.get("/products/filter/price", response_model=list[Product])
async def filter_products_by_price(
    min_price: float = Query(...),
    max_price: float = Query(...),
    db_pool: asyncpg.Pool = Depends(get_db),
) -> list[Product]:
    """
    Obtiene productos dentro de un rango de precio.
    """
    query = """
    SELECT id, name, price, quantity, description
    FROM products
    WHERE price BETWEEN $1 AND $2
    """
    try:
        async with db_pool.acquire() as conn:
            results = await conn.fetch(
                query,
                min_price,
                max_price
            )
            return [Product(**dict(result)) for result in results]
    except Exception as e:
        logger.error(f"Error al filtrar: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al filtrar productos"
        )