from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.constants import (
    BREED_OPTIONS,
    VACCINE_TYPES,
    ALLERGY_TYPES,
    SEVERITY_LEVELS,
    DIAGNOSIS_SEVERITY_LEVELS,
    MUCOUS_MEMBRANE_COLORS,
    EXAM_TYPES,
    LAB_REFERENCE_RANGES,
    ICD_VET_CODES,
    analyze_lab_exam
)
from app.models import Pet

router = APIRouter(prefix="/api/constants", tags=["constants"])


@router.get("/breeds")
def get_breeds(species: Optional[str] = None):
    if species:
        if species not in BREED_OPTIONS:
            return []
        return BREED_OPTIONS[species]
    return BREED_OPTIONS


@router.get("/vaccine-types")
def get_vaccine_types():
    return VACCINE_TYPES


@router.get("/allergy-types")
def get_allergy_types():
    return ALLERGY_TYPES


@router.get("/severity-levels")
def get_severity_levels():
    return SEVERITY_LEVELS


@router.get("/diagnosis-severity-levels")
def get_diagnosis_severity_levels():
    return DIAGNOSIS_SEVERITY_LEVELS


@router.get("/mucous-membrane-colors")
def get_mucous_membrane_colors():
    return MUCOUS_MEMBRANE_COLORS


@router.get("/exam-types")
def get_exam_types():
    return EXAM_TYPES


@router.get("/lab-reference-ranges")
def get_lab_reference_ranges(exam_type: Optional[str] = None):
    if exam_type:
        if exam_type not in LAB_REFERENCE_RANGES:
            return {}
        return LAB_REFERENCE_RANGES[exam_type]
    return LAB_REFERENCE_RANGES


@router.get("/icd-codes")
def get_icd_codes(category: Optional[str] = None, search: Optional[str] = None):
    codes = ICD_VET_CODES
    if category:
        codes = [c for c in codes if c["category"] == category]
    if search:
        search_lower = search.lower()
        codes = [
            c for c in codes
            if search_lower in c["code"].lower() or search_lower in c["name"].lower()
        ]
    return codes


@router.get("/icd-categories")
def get_icd_categories():
    categories = sorted(list({c["category"] for c in ICD_VET_CODES}))
    return categories


@router.post("/analyze-lab-exam/{record_id}")
def analyze_lab_exam_endpoint(
    record_id: int,
    exam_type: str,
    result_data: dict,
    db: Session = Depends(get_db)
):
    record = db.query(Pet).join(
        Pet.medical_records
    ).filter(
        Pet.medical_records.any(id=record_id)
    ).first()
    
    species = record.species if record else None
    
    if exam_type not in LAB_REFERENCE_RANGES:
        raise HTTPException(status_code=400, detail="Unsupported exam type")
    
    return analyze_lab_exam(exam_type, result_data, species)
