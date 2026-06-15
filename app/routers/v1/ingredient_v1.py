from app.services.v1.ingredient_service_v1 import IngredientServiceV1
from app.core.database import neo4j_db
from app.schemas.ingredient_schema import (
    CreateIngredientRequest,
    UpdateIngredientRequest
)
from app.schemas.effect_schema import HealthEffectRequest
from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients V1"]
)

ingredient_service = IngredientServiceV1(neo4j_db)


@router.get("/")
def list_ingredients():
    try:
        ingredients = ingredient_service.get_all_ingredients()

        return {
            "message": "Get Ingredients success",
            "data": ingredients,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_ingredient_by_id(id: str):
    try:
        ingredient = ingredient_service.get_ingredient_by_id(id)

        return {
            "message": "Get Ingredient success",
            "data": ingredient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
        
@router.get("/detail/{id}")
def get_ingredient_detail(id: str):
    try:
        ingredient = ingredient_service.get_ingredient_detail(id)

        return {
            "message": "Get Ingredient Detail success",
            "data": ingredient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_ingredient(payload: CreateIngredientRequest):
    try:
        ingredient = ingredient_service.create_ingredient(payload)

        return {
            "message": "Create Ingredient success",
            "data": ingredient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_ingredient(
    id: str,
    payload: UpdateIngredientRequest
):
    try:
        ingredient = ingredient_service.update_ingredient(
            ingredient_id=id,
            payload=payload
        )

        return {
            "message": "Update Ingredient success",
            "data": ingredient,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_ingredient(id: str):
    try:
        success = ingredient_service.delete_ingredient(
            ingredient_id=id
        )

        return {
            "message": "Delete Ingredient success",
            "data": success
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/health-effects/{ingredient_id}")
def attach_effect_to_ingredient(
    ingredient_id: str,
    payload: HealthEffectRequest
):
    try:
        result = ingredient_service.attach_effect_to_ingredient(
            ingredient_id,
            payload
        )

        return {
            "message": "Attach effect to ingredient success",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/food-categories/{ingredient_id}")
def attach_category_to_ingredient(
    ingredient_id: str,
    payload: HealthProfileRequest
):
    try:
        result = ingredient_service.attach_category_to_ingredient(
            ingredient_id,
            payload
        )

        return {
            "message": "Attach category to ingredient success",
            "data": result,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
