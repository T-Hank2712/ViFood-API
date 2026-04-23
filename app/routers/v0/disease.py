from fastapi import APIRouter
from app.services.v0.disease_service import DiseaseServiceV0

router = APIRouter(
    prefix="/diseases",
    tags=["Diseases V0"]
)

@router.get("/")
def list_diseases():
    return DiseaseServiceV0.get_all()