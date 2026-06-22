from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    species = Column(String(20), nullable=False)
    breed = Column(String(100))
    gender = Column(String(10), nullable=False)
    age = Column(Float)
    weight = Column(Float)
    fur_color = Column(String(50))
    neutered = Column(Boolean, default=False)
    owner_name = Column(String(100), nullable=False)
    owner_phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vaccines = relationship("Vaccine", back_populates="pet", cascade="all, delete-orphan")
    allergies = relationship("Allergy", back_populates="pet", cascade="all, delete-orphan")
    medical_records = relationship("MedicalRecord", back_populates="pet", cascade="all, delete-orphan")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    vaccine_type = Column(String(50), nullable=False)
    injection_date = Column(Date, nullable=False)
    brand = Column(String(100))
    batch_no = Column(String(100))
    next_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship("Pet", back_populates="vaccines")


class Allergy(Base):
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    allergy_type = Column(String(50), nullable=False)
    allergen = Column(String(100), nullable=False)
    reaction = Column(Text)
    severity = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pet = relationship("Pet", back_populates="allergies")


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    chief_complaint = Column(Text)
    present_illness = Column(Text)
    past_illness = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pet = relationship("Pet", back_populates="medical_records")
    clinical_exam = relationship("ClinicalExam", back_populates="record", uselist=False, cascade="all, delete-orphan")
    lab_exams = relationship("LabExam", back_populates="record", cascade="all, delete-orphan")
    diagnoses = relationship("Diagnosis", back_populates="record", cascade="all, delete-orphan")


class ClinicalExam(Base):
    __tablename__ = "clinical_exams"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False, unique=True)
    temperature = Column(Float)
    heart_rate = Column(Integer)
    respiratory_rate = Column(Integer)
    weight = Column(Float)
    body_condition_score = Column(Integer)
    mucous_membrane_color = Column(String(50))
    lymph_node_abnormality = Column(Text)
    cardio_pulmonary_auscultation = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    record = relationship("MedicalRecord", back_populates="clinical_exam")


class LabExam(Base):
    __tablename__ = "lab_exams"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False)
    exam_type = Column(String(50), nullable=False)
    result_data = Column(JSON)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    record = relationship("MedicalRecord", back_populates="lab_exams")


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False)
    icd_code = Column(String(50))
    diagnosis_name = Column(String(200), nullable=False)
    severity_level = Column(String(20), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    record = relationship("MedicalRecord", back_populates="diagnoses")
