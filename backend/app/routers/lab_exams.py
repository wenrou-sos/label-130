from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import MedicalRecord, LabExam, Pet
from app.schemas import LabExamCreate, LabExamUpdate, LabExamResponse
from app.constants import analyze_lab_exam

router = APIRouter(prefix="/api", tags=["lab_exams"])


def get_species_for_record(record_id: int, db: Session) -> Optional[str]:
    pet = db.query(Pet).join(
        Pet.medical_records
    ).filter(
        Pet.medical_records.any(id=record_id)
    ).first()
    return pet.species if pet else None


@router.get("/medical-records/{record_id}/lab-exams")
def list_lab_exams(record_id: int, include_analysis: bool = True, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    exams = db.query(LabExam).filter(LabExam.record_id == record_id).all()
    species = get_species_for_record(record_id, db) if include_analysis else None
    
    result = []
    for exam in exams:
        exam_dict = {
            "id": exam.id,
            "record_id": exam.record_id,
            "exam_type": exam.exam_type,
            "result_data": exam.result_data,
            "notes": exam.notes,
            "created_at": exam.created_at
        }
        if include_analysis and exam.result_data:
            exam_dict["analysis"] = analyze_lab_exam(exam.exam_type, exam.result_data, species)
        result.append(exam_dict)
    
    return result


@router.post("/medical-records/{record_id}/lab-exams", response_model=LabExamResponse, status_code=201)
def create_lab_exam(record_id: int, exam_in: LabExamCreate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    exam = LabExam(**exam_in.model_dump(), record_id=record_id)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.put("/lab-exams/{exam_id}", response_model=LabExamResponse)
def update_lab_exam(exam_id: int, exam_in: LabExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(LabExam).filter(LabExam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Lab exam not found")
    update_data = exam_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exam, key, value)
    db.commit()
    db.refresh(exam)
    return exam


@router.delete("/lab-exams/{exam_id}", status_code=204)
def delete_lab_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(LabExam).filter(LabExam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Lab exam not found")
    db.delete(exam)
    db.commit()
