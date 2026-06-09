"""
Product Models
Schema cho product response
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductNutrition(BaseModel):
    energy: Optional[str] = Field(default=None, example="450 kcal")
    protein: Optional[str] = Field(default=None, example="12 g")
    fat: Optional[str] = Field(default=None, example="18 g")
    sugar: Optional[str] = Field(default=None, example="20 g")


class Product(BaseModel):
    id: int = Field(..., alias="_id", example=123)
    user_id: int = Field(..., example=1)
    product_name: str = Field(..., example="Sữa ABC")

    age_range: Optional[str] = Field(default=None, example="1-3 tuổi")

    ingredients: List[str] = Field(
        default_factory=list,
        example=["Sữa bột", "Đường", "Dầu thực vật"]
    )

    additive: List[str] = Field(
        default_factory=list,
        example=["Chất điều vị (INS 621)"]
    )

    nutrition: ProductNutrition

    manufacturer: Optional[str] = Field(default=None, example="Công ty XYZ")

    mfg_date: Optional[str] = Field(default=None, example="2025-12-31")
    expiry_date: Optional[str] = Field(default=None, example="2027-12-31")

    net_weight: Optional[str] = Field(default=None, example="900g")

    allergen: Optional[str] = Field(default=None, example="Sản phẩm có chứa sữa")

    warning: Optional[str] = Field(default=None, example="Không sử dụng cho trẻ em dưới 3 tuổi")

    origin: Optional[str] = Field(default=None, example="Việt Nam")

    createdAt: datetime = Field(..., example="2026-06-09T05:27:07.241790Z")
    timeZone: str = Field(..., example="Asia/Ho_Chi_Minh")
    createdAtLocal: datetime = Field(..., example="2026-06-09T12:27:07.241790+07:00")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": 123,
                "product_name": "Sữa ABC",
                "age_range": "1-3 tuổi",
                "ingredients": ["Sữa bột", "Đường", "Dầu thực vật"],
                "additive": ["Chất điều vị (INS 621)"],
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
        
        
class ProductCreate(BaseModel):
    product_name: str
    age_range: Optional[str] = None
    ingredients: List[str] = Field(default_factory=list)
    additive: List[str] = Field(default_factory=list)
    nutrition: Optional[ProductNutrition] = None
    manufacturer: Optional[str] = None
    mfg_date: Optional[str] = None
    expiry_date: Optional[str] = None
    net_weight: Optional[str] = None
    allergen: Optional[str] = None
    warning: Optional[str] = None
    origin: Optional[str] = None
