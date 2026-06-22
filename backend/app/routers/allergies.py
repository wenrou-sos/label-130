from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pet, Allergy
from app.schemas import AllergyCreate, AllergyUpdate, AllergyResponse

router = APIRouter(prefix="/api", tags=["allergies"])


@router.get("/pets/{pet_id}/allergies", response_model=list[AllergyResponse])
def list_allergies(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db.query(Allergy).filter(Allergy.pet_id == pet_id).all()


@router.post("/pets/{pet_id}/allergies", response_model=AllergyResponse, status_code=201)
def create_allergy(pet_id: int, allergy_in: AllergyCreate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    allergy = Allergy(**allergy_in.model_dump(), pet_id=pet_id)
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy


@router.put("/allergies/{allergy_id}", response_model=AllergyResponse)
def update_allergy(allergy_id: int, allergy_in: AllergyUpdate, db: Session = Depends(get_db)):
    allergy = db.query(Allergy).filter(Allergy.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    update_data = allergy_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(allergy, key, value)
    db.commit()
    db.refresh(allergy)
    return allergy


@router.delete("/allergies/{allergy_id}", status_code=204)
def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    allergy = db.query(Allergy).filter(Allergy.id == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    db.delete(allergy)
    db.commit()
