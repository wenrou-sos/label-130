from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MedicalRecord, ClinicalExam
from app.schemas import ClinicalExamCreate, ClinicalExamUpdate, ClinicalExamResponse

router = APIRouter(prefix="/api", tags=["clinical_exams"])


@router.get("/medical-records/{record_id}/clinical-exam", response_model=ClinicalExamResponse)
def get_clinical_exam(record_id: int, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    exam = db.query(ClinicalExam).filter(ClinicalExam.record_id == record_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Clinical exam not found")
    return exam


@router.post("/medical-records/{record_id}/clinical-exam", response_model=ClinicalExamResponse, status_code=201)
def create_clinical_exam(record_id: int, exam_in: ClinicalExamCreate, db: Session = Depends(get_db)):
    record = db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    existing = db.query(ClinicalExam).filter(ClinicalExam.record_id == record_id).first()
    if existing:
        raise HTTPException(status_code=422, detail="Clinical exam already exists for this record")
    exam = ClinicalExam(**exam_in.model_dump(), record_id=record_id)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.put("/clinical-exams/{exam_id}", response_model=ClinicalExamResponse)
def update_clinical_exam(exam_id: int, exam_in: ClinicalExamUpdate, db: Session = Depends(get_db)):
    exam = db.query(ClinicalExam).filter(ClinicalExam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Clinical exam not found")
    update_data = exam_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exam, key, value)
    db.commit()
    db.refresh(exam)
    return exam
