from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# "Base de datos" falsa en memoria
pets = []

# Modelo de datos
class Pet(BaseModel):
    id: int
    name: str
    type: str
    age: int

# Ruta inicial
@app.get("/")
def home():
    return {"msg": "API PetShop funcionando"}

# Obtener todas las mascotas
@app.get("/pets")
def get_pets():
    return pets

# Obtener mascota por id
@app.get("/pets/{pet_id}")
def get_pet(pet_id: int):
    for pet in pets:
        if pet.id == pet_id:
            return pet
    return {"error": "Mascota no encontrada"}

# Crear mascota
@app.post("/pets")
def create_pet(pet: Pet):
    pets.append(pet)
    return {"msg": "Mascota creada", "pet": pet}

# Actualizar mascota
@app.put("/pets/{pet_id}")
def update_pet(pet_id: int, updated_pet: Pet):
    for i, pet in enumerate(pets):
        if pet.id == pet_id:
            pets[i] = updated_pet
            return {"msg": "Mascota actualizada"}
    return {"error": "Mascota no encontrada"}

# Eliminar mascota
@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int):
    for pet in pets:
        if pet.id == pet_id:
            pets.remove(pet)
            return {"msg": "Mascota eliminada"}
    return {"error": "Mascota no encontrada"}
