from app.services.v1.additive_service_v1 import AdditiveServiceV1
from app.core.database import neo4j_db
from app.schemas.additive_schema import (
    CreateAdditiveRequest,
    UpdateAdditiveRequest
)
from app.schemas.effect_schema import HealthEffectRequest
from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/additives",
    tags=["Additives V1"]
)

additive_service = AdditiveServiceV1(neo4j_db)


@router.get("/")
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


@router.get("/{id}")
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


@router.post("/")
def create_additive(payload: CreateAdditiveRequest):
    try:
        additive = additive_service.create_additive(payload)

        return {
            "message": "Create Additive success",
            "data": additive,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_additive(
    id: str,
    payload: UpdateAdditiveRequest
):
    try:
        additive = additive_service.update_additive(
            additive_id=id,
            payload=payload
        )

        return {
            "message": "Update Additive success",
            "data": additive,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_additive(id: str):
    try:
        success = additive_service.delete_additive(
            additive_id=id
        )

        return {
            "message": "Delete Additive success",
            "data": success
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/health-effects/{additive_id}")
def attach_effect_to_additive(
    additive_id: str,
    payload: HealthEffectRequest
):
    try:
        result = additive_service.attach_effect_to_additive(
            additive_id,
            payload
        )

        return {
            "message": "Attach effect to additive success",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/food-categories/{additive_id}")
def attach_category_to_additive(
    additive_id: str,
    payload: HealthProfileRequest
):
    try:
        result = additive_service.attach_category_to_additive(
            additive_id,
            payload
        )

        return {
            "message": "Attach category to additive success",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
