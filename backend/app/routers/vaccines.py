from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pet, Vaccine
from app.schemas import VaccineCreate, VaccineUpdate, VaccineResponse

router = APIRouter(prefix="/api", tags=["vaccines"])


@router.get("/pets/{pet_id}/vaccines", response_model=list[VaccineResponse])
def list_vaccines(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db.query(Vaccine).filter(Vaccine.pet_id == pet_id).all()


@router.post("/pets/{pet_id}/vaccines", response_model=VaccineResponse, status_code=201)
def create_vaccine(pet_id: int, vaccine_in: VaccineCreate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    vaccine = Vaccine(**vaccine_in.model_dump(), pet_id=pet_id)
    db.add(vaccine)
    db.commit()
    db.refresh(vaccine)
    return vaccine


@router.put("/vaccines/{vaccine_id}", response_model=VaccineResponse)
def update_vaccine(vaccine_id: int, vaccine_in: VaccineUpdate, db: Session = Depends(get_db)):
    vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    update_data = vaccine_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vaccine, key, value)
    db.commit()
    db.refresh(vaccine)
    return vaccine


@router.delete("/vaccines/{vaccine_id}", status_code=204)
def delete_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(Vaccine).filter(Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    db.delete(vaccine)
    db.commit()
