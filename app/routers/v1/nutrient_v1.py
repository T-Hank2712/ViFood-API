from fastapi import APIRouter, HTTPException, status

from app.core.database import neo4j_db
from app.schemas.nutrient_v1_schema import (
    NutrientDetailApiResponse,
    NutrientListApiResponse,
)
from app.services.v1.nutrient_service_v1 import NutrientServiceV1

router = APIRouter(
    prefix="/nutrients",
    tags=["Nutrients V1"]
)

nutrient_service = NutrientServiceV1(neo4j_db)


@router.get("/", response_model=NutrientListApiResponse)
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


@router.get("/{id}", response_model=NutrientDetailApiResponse)
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
