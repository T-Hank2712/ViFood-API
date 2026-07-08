from fastapi import APIRouter, HTTPException, status

from app.core.database import neo4j_db
from app.schemas.additive_v1_schema import (
    AdditiveDetailApiResponse,
    AdditiveListApiResponse,
)
from app.services.v1.additive_service_v1 import AdditiveServiceV1

router = APIRouter(
    prefix="/additives",
    tags=["Additives V1"]
)

additive_service = AdditiveServiceV1(neo4j_db)


@router.get("/", response_model=AdditiveListApiResponse)
def list_additives():
    try:
        additives = additive_service.get_all_additives()

        return {
            "message": "Get Additives success",
            "data": additives,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}", response_model=AdditiveDetailApiResponse)
def get_additive_by_id(id: str):
    try:
        additive = additive_service.get_additive_by_id(id)

        return {
            "message": "Get Additive success",
            "data": additive,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
