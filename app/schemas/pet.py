from pydantic import BaseModel, Field


class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Buddy"])
    type: str = Field(..., min_length=1, max_length=50, examples=["dog"])
    age: int = Field(..., ge=0, le=100, examples=[3])


class PetCreate(PetBase):
    """Schema for creating a new pet (no id required)."""
    pass


class PetUpdate(PetBase):
    """Schema for fully updating an existing pet."""
    pass


class PetResponse(PetBase):
    """Schema returned to the client — includes the database-assigned id."""
    id: int

    model_config = {"from_attributes": True}
