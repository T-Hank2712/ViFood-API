from app.services.v1.health_effect_service_v1 import HealthEffectServiceV1
from app.core.database import neo4j_db
from app.schemas.effect_schema import HealthEffectRequest

from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/health-effects",
    tags=["Health Effects V1"]
)

health_effect_service = HealthEffectServiceV1(neo4j_db)


@router.get("/")
def list_health_effects():
    try:
        effects = health_effect_service.get_all_health_effects()

        return {
            "message": "Get Health Effects success",
            "data": effects,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_health_effect_by_id(id: str):
    try:
        effect = health_effect_service.get_health_effect_by_id(id)

        return {
            "message": "Get Health Effect success",
            "data": effect,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_health_effect(payload: HealthEffectRequest):
    try:
        effect = health_effect_service.create_health_effect(
            name=payload.name,
            description=payload.description
        )

        return {
            "message": "Create Health Effect success",
            "data": effect,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_health_effect(
    id: str,
    payload: HealthEffectRequest
):
    try:
        effect = health_effect_service.update_health_effect(
            effect_id=id,
            payload=payload
        )

        return {
            "message": "Update Health Effect success",
            "data": effect,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_health_effect(id: str):
    try:
        success = health_effect_service.delete_health_effect(
            effect_id=id
        )

        return {
            "message": "Delete Health Effect success",
            "data": success
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
