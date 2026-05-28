from pydantic import BaseModel, Field, ConfigDict


# 1️⃣ Modelo completo (representa la tabla)
class Product(BaseModel):
    """Representa un producto completo (con id)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    quantity: int
    description: str | None


# 2️⃣ Para CREAR (sin id, lo genera la BD)
class ProductCreate(BaseModel):
    """Datos necesarios para crear un producto."""
    name: str
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    description: str | None = Field(None, max_length=255)


# 3️⃣ Para ACTUALIZAR (todo opcional)
class ProductUpdate(BaseModel):
    """Datos opcionales para actualizar."""
    name: str | None = None
    price: float | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)
    description: str | None = Field(None, max_length=255)


# 4️⃣ Para actualizar solo STOCK
class ProductStockUpdate(BaseModel):
    """Solo actualiza la cantidad."""
    quantity: int = Field(..., ge=0)