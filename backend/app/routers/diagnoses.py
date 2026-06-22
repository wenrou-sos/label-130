from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MedicalRecord, Diagnosis
from app.schemas import DiagnosisCreate, DiagnosisUpdate, DiagnosisResponse

router = APIRouter(prefix="/api", tags=["diagnoses"])


@router.get("/medical-records/{record_id}/diagnoses", response_model=list[DiagnosisResponse])
def list_diagnoses(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    return db.query(Diagnosis).filter(Diagnosis.record_id == record_id).all()


@router.post("/medical-records/{record_id}/diagnoses", response_model=DiagnosisResponse, status_code=201)
def create_diagnosis(record_id: int, diagnosis_in: DiagnosisCreate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    diagnosis = Diagnosis(**diagnosis_in.model_dump(), record_id=record_id)
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis


@router.put("/diagnoses/{diagnosis_id}", response_model=DiagnosisResponse)
def update_diagnosis(diagnosis_id: int, diagnosis_in: DiagnosisUpdate, db: Session = Depends(get_db)):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    update_data = diagnosis_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(diagnosis, key, value)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis


@router.delete("/diagnoses/{diagnosis_id}", status_code=204)
def delete_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    db.delete(diagnosis)
    db.commit()
