from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.pet import PetCreate, PetResponse, PetUpdate
from app.services import pet_service

router = APIRouter(prefix="/pets", tags=["Pets"])


@router.get("/", response_model=list[PetResponse])
def list_pets(db: Session = Depends(get_db)):
    """Return all pets."""
    return pet_service.get_all_pets(db)


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """Return a single pet by id."""
    pet = pet_service.get_pet_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(payload: PetCreate, db: Session = Depends(get_db)):
    """Create a new pet."""
    return pet_service.create_pet(db, payload)


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, payload: PetUpdate, db: Session = Depends(get_db)):
    """Fully update an existing pet."""
    pet = pet_service.update_pet(db, pet_id, payload)
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    return pet


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """Delete a pet. Returns 204 No Content on success."""
    deleted = pet_service.delete_pet(db, pet_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
