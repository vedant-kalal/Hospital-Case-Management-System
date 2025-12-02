from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from .routes.health_center_routes import router as health_router
from .routes.clinician_routes import router as clinician_router
from .routes.patient_case_routes import router as patient_case_router
from .routes.case_note_routes import router as case_note_router
from src.models import user, health_center, clinician, patient_case, case_note


app = FastAPI(title="Hospital Case Management API")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(clinician_router, prefix="/api/v1")
app.include_router(patient_case_router, prefix="/api/v1")
app.include_router(case_note_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API Running!"}
