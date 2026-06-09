from typing import Literal
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, examples=["Dog Food Premium"])
    description: str | None = Field(None, max_length=500, examples=["High quality food for adult dogs"])
    price: float = Field(..., gt=0.0, examples=[25.99])
    stock: int = Field(..., ge=0, examples=[50])
    category: Literal["food", "toys", "accessories", "medicine"] = Field(
        ..., 
        examples=["food"],
        description="Must be one of: food, toys, accessories, medicine"
    )
    pet_type: str = Field(..., min_length=1, max_length=50, examples=["dog"])


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(ProductBase):
    """Schema for updating an existing product."""
    pass


class ProductResponse(ProductBase):
    """Schema returned to the client — includes the database-assigned id."""
    id: int
    model_config = {"from_attributes": True}
