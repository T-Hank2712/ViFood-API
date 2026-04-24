from fastapi import APIRouter
from app.services.v0.disease_service import DiseaseServiceV0

router = APIRouter(
    prefix="/diseases",
    tags=["Diseases V0"]
)

@router.get("/")
def list_diseases():
    return DiseaseServiceV0.get_all()

@router.get("/{id}")
def get_disease_by_id(id: int):
    disease = DiseaseServiceV0.get_by_id(id)
    return disease or {"error": "Disease not found"}

@router.post("/")
def create_disease(name: str):
    new_disease = DiseaseServiceV0.create_disease(name)
    return new_disease

@router.put("/{id}")
def update_disease(id: int, name: str):
    updated_disease = DiseaseServiceV0.update_disease(id, name)
    if updated_disease:
        return updated_disease
    return {"error": "Disease not found"}

@router.delete("/{id}")
def delete_disease(id: int):
    result = DiseaseServiceV0.delete_disease(id)
    return result