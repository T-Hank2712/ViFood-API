"""
Product Models
Schema cho product response
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductNutrition(BaseModel):
    energy: str = Field(..., example="450 kcal")
    protein: str = Field(..., example="12 g")
    fat: str = Field(..., example="18 g")
    sugar: str = Field(..., example="20 g")


class ProductResponse(BaseModel):
    id: int = Field(..., alias="_id", example=123)
    product_name: str = Field(..., example="Sữa ABC")
    age_range: str = Field(..., example="1-3 tuổi")
    ingredients: List[str] = Field(..., example=["Sữa bột", "Đường", "Dầu thực vật"])
    additive: Optional[List[str]] = Field(default=None, example=["Chất điều vị (INS 621)"])
    nutrition: ProductNutrition
    manufacturer: str = Field(..., example="Công ty XYZ")
    mfg_date: str = Field(..., example="2025-12-31")
    expiry_date: str = Field(..., example="2027-12-31")
    net_weight: str = Field(..., example="900g")
    allergen: str = Field(..., example="Sản phẩm có chứa sữa")
    warning: str = Field(..., example="Không sử dụng cho trẻ em dưới 3 tuổi")
    origin: str = Field(..., example="Việt Nam")
    createdAt: datetime = Field(..., example="2026-03-02T13:16:00.955Z")
    timeZone: str = Field(..., example="Asia/Ho_Chi_Minh")
    createdAtLocal: str = Field(..., example="2026-03-02 20:16:00")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": 123,
                "product_name": "Sữa ABC",
                "age_range": "1-3 tuổi",
                "ingredients": [
                    "Sữa bột",
                    "Đường",
                    "Dầu thực vật"
                ],
                "additive": [
                    "Chất điều vị (INS 621)"
                ],
                "nutrition": {
                    "energy": "450 kcal",
                    "protein": "12 g",
                    "fat": "18 g",
                    "sugar": "20 g"
                },
                "manufacturer": "Công ty XYZ",
                "mfg_date": "2025-12-31",
                "expiry_date": "2027-12-31",
                "net_weight": "900g",
                "allergen": "Sản phẩm có chứa sữa",
                "warning": "Không sử dụng cho trẻ em dưới 3 tuổi",
                "origin": "Việt Nam",
                "createdAt": "2026-03-02T13:16:00.955Z",
                "timeZone": "Asia/Ho_Chi_Minh",
                "createdAtLocal": "2026-03-02 20:16:00"
            }
        }
