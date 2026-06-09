from pydantic import BaseModel, Field

# 1. Schema for user creation (Registration and Login)
class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=72)

# 2. Schema to safely display user data
class UserOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}  # Allows reading SQLAlchemy objects directly

# 3. Response schema when login is successful
class Token(BaseModel):
    access_token: str
    token_type: str

# 4. Schema for internal payload traveling within the JWT
class TokenData(BaseModel):
    username: str | None = None
