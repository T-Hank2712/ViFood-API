from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    product_name: Optional[str] = None

    age_range: Optional[str] = None

    ingredients: List[str] = Field(default_factory=list)

    additive: List[str] = Field(default_factory=list)

    nutrition: Dict[str, str] = Field(default_factory=dict)

    manufacturer: Optional[str] = None

    mfg_date: Optional[str] = None

    expiry_date: Optional[str] = None

    net_weight: Optional[str] = None

    allergen: Optional[str] = None

    warning: Optional[str] = None

    origin: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
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
                "origin": "Việt Nam"
            }
        }
    }


class ProductCreate(BaseModel):
    product_name: Optional[str] = None

    age_range: Optional[str] = None

    ingredients: List[str] = Field(default_factory=list)

    additive: List[str] = Field(default_factory=list)

    nutrition: Dict[str, str] = Field(default_factory=dict)

    manufacturer: Optional[str] = None

    mfg_date: Optional[str] = None

    expiry_date: Optional[str] = None

    net_weight: Optional[str] = None

    allergen: Optional[str] = None

    warning: Optional[str] = None

    origin: Optional[str] = None
