from pydantic import BaseModel, Field

# 1. Esquema para la creación de usuarios (Registro e Login)
class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=72)

# 2. Esquema para mostrar los datos del usuario de forma segura
class UserOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}  # Permite leer objetos de SQLAlchemy directamente

# 3. Esquema de respuesta cuando el login es exitoso
class Token(BaseModel):
    access_token: str
    token_type: str

# 4. Esquema para el contenido interno que viaja dentro del JWT (Payload)
class TokenData(BaseModel):
    username: str | None = None
