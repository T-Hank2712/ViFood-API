from app.services.v1.disease_service_v1 import DiseaseServiceV1
from app.core.database import neo4j_db
from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/diseases",
    tags=["Diseases V1"]
)

disease_service = DiseaseServiceV1(neo4j_db)


@router.get("/")
def list_diseases():
    try:
        diseases = disease_service.get_all_diseases()

        return {
            "message": "Get Diseases success",
            "data": diseases,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_disease_by_id(id: str):
    try:
        disease = disease_service.get_disease_by_id(id)

        return {
            "message": "Get Disease success",
            "data": disease,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_disease(payload: HealthProfileRequest):
    try:
        disease = disease_service.create_disease(payload.name)

        return {
            "message": "Create Disease success",
            "data": disease,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_disease(id: str, payload: HealthProfileRequest):
    try:
        disease = disease_service.update_disease(
            disease_id=id,
            name=payload.name,
        )

        return {
            "message": "Update Disease success",
            "data": disease,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_disease(id: str):
    try:
        disease_service.delete_disease(disease_id=id)

        return {
            "message": "Delete Disease success"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
