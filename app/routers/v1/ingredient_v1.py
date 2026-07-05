from fastapi import APIRouter, HTTPException, status

from app.core.database import neo4j_db
from app.schemas.wiki_node_schema import WikiNodeApiResponse, WikiNodeListApiResponse
from app.services.v1.ingredient_service_v1 import IngredientServiceV1

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients V1"]
)

ingredient_service = IngredientServiceV1(neo4j_db)


@router.get("/", response_model=WikiNodeListApiResponse)
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


@router.get("/{id}", response_model=WikiNodeApiResponse)
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
