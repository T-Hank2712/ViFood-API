from app.services.v1.nutrient_service_v1 import NutrientServiceV1
from app.core.database import neo4j_db
from app.schemas.nutrient_schema import CreateNutrientRequest, UpdateNutrientRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/nutrients",
    tags=["Nutrients V1"]
)

nutrient_service = NutrientServiceV1(neo4j_db)


@router.get("/")
def list_nutrients():
    try:
        nutrients = nutrient_service.get_all_nutrients()

        return {
            "message": "Get Nutrients success",
            "data": nutrients,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_nutrient_by_id(id: str):
    try:
        nutrient = nutrient_service.get_nutrient_by_id(id)

        return {
            "message": "Get Nutrient success",
            "data": nutrient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_nutrient(payload: CreateNutrientRequest):
    try:
        nutrient = nutrient_service.create_nutrient(payload)

        return {
            "message": "Create Nutrient success",
            "data": nutrient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_nutrient(id: str, payload: UpdateNutrientRequest):
    try:
        nutrient = nutrient_service.update_nutrient(
            nutrient_id=id,
            payload=payload
        )

        return {
            "message": "Update Nutrient success",
            "data": nutrient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_nutrient(id: str):
    try:
        success = nutrient_service.delete_nutrient(nutrient_id=id)

        return {
            "message": "Delete Nutrient success",
            "data": success
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
