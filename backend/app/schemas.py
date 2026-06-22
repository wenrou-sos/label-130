from datetime import date, datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict


class PetCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    gender: str
    age: Optional[float] = None
    weight: Optional[float] = None
    fur_color: Optional[str] = None
    neutered: Optional[bool] = False
    owner_name: str
    owner_phone: str


class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[float] = None
    weight: Optional[float] = None
    fur_color: Optional[str] = None
    neutered: Optional[bool] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None


class PetResponse(BaseModel):
    id: int
    name: str
    species: str
    breed: Optional[str] = None
    gender: str
    age: Optional[float] = None
    weight: Optional[float] = None
    fur_color: Optional[str] = None
    neutered: Optional[bool] = False
    owner_name: str
    owner_phone: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PetListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[PetResponse]


class VaccineCreate(BaseModel):
    vaccine_type: str
    injection_date: date
    brand: Optional[str] = None
    batch_no: Optional[str] = None
    next_date: Optional[date] = None


class VaccineUpdate(BaseModel):
    vaccine_type: Optional[str] = None
    injection_date: Optional[date] = None
    brand: Optional[str] = None
    batch_no: Optional[str] = None
    next_date: Optional[date] = None


class VaccineResponse(BaseModel):
    id: int
    pet_id: int
    vaccine_type: str
    injection_date: date
    brand: Optional[str] = None
    batch_no: Optional[str] = None
    next_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AllergyCreate(BaseModel):
    allergy_type: str
    allergen: str
    reaction: Optional[str] = None
    severity: str


class AllergyUpdate(BaseModel):
    allergy_type: Optional[str] = None
    allergen: Optional[str] = None
    reaction: Optional[str] = None
    severity: Optional[str] = None


class AllergyResponse(BaseModel):
    id: int
    pet_id: int
    allergy_type: str
    allergen: str
    reaction: Optional[str] = None
    severity: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordCreate(BaseModel):
    visit_date: date
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    past_illness: Optional[str] = None
    notes: Optional[str] = None


class MedicalRecordUpdate(BaseModel):
    visit_date: Optional[date] = None
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    past_illness: Optional[str] = None
    notes: Optional[str] = None


class ClinicalExamResponse(BaseModel):
    id: int
    record_id: int
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    body_condition_score: Optional[int] = None
    mucous_membrane_color: Optional[str] = None
    lymph_node_abnormality: Optional[str] = None
    cardio_pulmonary_auscultation: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiagnosisResponse(BaseModel):
    id: int
    record_id: int
    icd_code: Optional[str] = None
    diagnosis_name: str
    severity_level: str
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LabExamResponse(BaseModel):
    id: int
    record_id: int
    exam_type: str
    result_data: Optional[Any] = None
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordResponse(BaseModel):
    id: int
    pet_id: int
    visit_date: date
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    past_illness: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    clinical_exam: Optional[ClinicalExamResponse] = None
    diagnoses: Optional[List[DiagnosisResponse]] = None
    lab_exams: Optional[List[LabExamResponse]] = None

    model_config = ConfigDict(from_attributes=True)


class ClinicalExamCreate(BaseModel):
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    body_condition_score: Optional[int] = None
    mucous_membrane_color: Optional[str] = None
    lymph_node_abnormality: Optional[str] = None
    cardio_pulmonary_auscultation: Optional[str] = None


class ClinicalExamUpdate(BaseModel):
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    body_condition_score: Optional[int] = None
    mucous_membrane_color: Optional[str] = None
    lymph_node_abnormality: Optional[str] = None
    cardio_pulmonary_auscultation: Optional[str] = None


class LabExamCreate(BaseModel):
    exam_type: str
    result_data: Optional[Any] = None
    notes: Optional[str] = None


class LabExamUpdate(BaseModel):
    exam_type: Optional[str] = None
    result_data: Optional[Any] = None
    notes: Optional[str] = None


class DiagnosisCreate(BaseModel):
    icd_code: Optional[str] = None
    diagnosis_name: str
    severity_level: str
    notes: Optional[str] = None


class DiagnosisUpdate(BaseModel):
    icd_code: Optional[str] = None
    diagnosis_name: Optional[str] = None
    severity_level: Optional[str] = None
    notes: Optional[str] = None
