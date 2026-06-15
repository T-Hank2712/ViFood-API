from fastapi import APIRouter, HTTPException, status
from app.services.v1.search_service_v1 import SearchServiceV1
from app.core.database import neo4j_db

router = APIRouter(
    prefix="/search",
    tags=["Search Nutrition V1"]
)


search_service = SearchServiceV1(neo4j_db)


@router.get("/", summary="Lấy danh sách nutrition, ingredient, additive")
def get_nutritions():
    nutritions = search_service.get_all()
    return {
            "message": "Get All Nutri success",
            "data": nutritions,
        }


@router.get("/{id}", summary="Lấy chi tiết nutrition theo ID")
def get_nutrition_by_id(
    id: str
):
    result = search_service.get_by_id(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
        
    return {
            "message": "Get Nutri Detail success",
            "data": result,
        }
