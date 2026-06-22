from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Pet
from app.schemas import PetCreate, PetUpdate, PetResponse, PetListResponse

router = APIRouter(prefix="/api/pets", tags=["pets"])


@router.get("", response_model=PetListResponse)
def list_pets(
    species: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Pet)
    if species:
        query = query.filter(Pet.species == species)
    if search:
        query = query.filter(
            (Pet.name.ilike(f"%{search}%"))
            | (Pet.owner_name.ilike(f"%{search}%"))
            | (Pet.owner_phone.ilike(f"%{search}%"))
        )
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PetListResponse(total=total, page=page, page_size=page_size, items=items)


@router.post("", response_model=PetResponse, status_code=201)
def create_pet(pet_in: PetCreate, db: Session = Depends(get_db)):
    pet = Pet(**pet_in.model_dump())
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/{pet_id}", response_model=PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, pet_in: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    update_data = pet_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pet, key, value)
    db.commit()
    db.refresh(pet)
    return pet


@router.delete("/{pet_id}", status_code=204)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
