from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Pet, MedicalRecord
from app.schemas import MedicalRecordCreate, MedicalRecordUpdate, MedicalRecordResponse

router = APIRouter(prefix="/api", tags=["medical_records"])


@router.get("/pets/{pet_id}/medical-records", response_model=list[MedicalRecordResponse])
def list_medical_records(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db.query(MedicalRecord).filter(MedicalRecord.pet_id == pet_id).all()


@router.post("/pets/{pet_id}/medical-records", response_model=MedicalRecordResponse, status_code=201)
def create_medical_record(pet_id: int, record_in: MedicalRecordCreate, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    record = MedicalRecord(**record_in.model_dump(), pet_id=pet_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/medical-records/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return record


@router.put("/medical-records/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(record_id: int, record_in: MedicalRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    update_data = record_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/medical-records/{record_id}", status_code=204)
def delete_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    db.delete(record)
    db.commit()
