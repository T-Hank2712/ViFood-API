from app.services.v1.food_category_service_v1 import FoodCategoryServiceV1
from app.core.database import neo4j_db
from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/food-categories",
    tags=["Food Categories V1"]
)

food_category_service = FoodCategoryServiceV1(neo4j_db)


@router.get("/")
def list_food_categories():
    try:
        categories = food_category_service.get_all_food_categories()

        return {
            "message": "Get Food Categories success",
            "data": categories,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_food_category_by_id(id: str):
    try:
        category = food_category_service.get_food_category_by_id(id)

        return {
            "message": "Get Food Category success",
            "data": category,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_food_category(payload: HealthProfileRequest):
    try:
        category = food_category_service.create_food_category(payload.name)

        return {
            "message": "Create Food Category success",
            "data": category,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_food_category(id: str, payload: HealthProfileRequest):
    try:
        category = food_category_service.update_food_category(
            category_id=id,
            name=payload.name,
        )

        return {
            "message": "Update Food Category success",
            "data": category,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{id}")
def delete_food_category(id: str):
    try:
        success = food_category_service.delete_food_category(
            category_id=id
        )

        return {
            "message": "Delete Food Category success",
            "data": success
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
