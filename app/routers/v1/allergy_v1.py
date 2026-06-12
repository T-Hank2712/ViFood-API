from app.services.v1.allergy_service_v1 import AllergyServiceV1
from app.core.database import neo4j_db
from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies V1"]
)

allergy_service = AllergyServiceV1(neo4j_db)


@router.get("/")
def list_allergies():
    try:
        allergies = allergy_service.get_all_allergies()

        return {
            "message": "Get Allergies success",
            "data": allergies,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_allergy_by_id(id: str):
    try:
        allergy = allergy_service.get_allergy_by_id(id)

        return {
            "message": "Get Allergy success",
            "data": allergy,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_allergy(payload: HealthProfileRequest):
    try:
        allergy = allergy_service.create_allergy(payload.name)

        return {
            "message": "Create Allergy success",
            "data": allergy,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_allergy(id: str, payload: HealthProfileRequest):
    try:
        allergy = allergy_service.update_allergy(
            allergy_id=id,
            name=payload.name,
        )

        return {
            "message": "Update Allergy success",
            "data": allergy,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_allergy(id: str):
    try:
        allergy_service.delete_allergy(allergy_id=id)

        return {
            "message": "Delete Allergy success"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
