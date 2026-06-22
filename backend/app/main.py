from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import pets, vaccines, allergies, medical_records, clinical_exams, lab_exams, diagnoses, constants

app = FastAPI(title="Pet Hospital EMR System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets.router)
app.include_router(vaccines.router)
app.include_router(allergies.router)
app.include_router(medical_records.router)
app.include_router(clinical_exams.router)
app.include_router(lab_exams.router)
app.include_router(diagnoses.router)
app.include_router(constants.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
