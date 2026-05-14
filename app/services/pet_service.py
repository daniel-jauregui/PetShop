from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate


def get_all_pets(db: Session, name: str | None = None, type: str | None = None, age: int | None = None) -> list[Pet]:
    query = db.query(Pet)
    if name:
        query = query.filter(Pet.name.ilike(f"%{name}%"))
    if type:
        query = query.filter(Pet.type.ilike(f"%{type}%"))
    if age is not None:
        query = query.filter(Pet.age == age)
    return query.all()


def get_pet_by_id(db: Session, pet_id: int) -> Pet | None:
    return db.query(Pet).filter(Pet.id == pet_id).first()


def create_pet(db: Session, data: PetCreate) -> Pet:
    pet = Pet(**data.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


def update_pet(db: Session, pet_id: int, data: PetUpdate) -> Pet | None:
    pet = get_pet_by_id(db, pet_id)
    if not pet:
        return None
    for field, value in data.model_dump().items():
        setattr(pet, field, value)
    db.commit()
    db.refresh(pet)
    return pet


def delete_pet(db: Session, pet_id: int) -> bool:
    pet = get_pet_by_id(db, pet_id)
    if not pet:
        return False
    db.delete(pet)
    db.commit()
    return True
