"""
Products Router V0
Base API trả dữ liệu mẫu product (không truy vấn DB).
"""
from fastapi import APIRouter

from app.models.product import ProductResponse
from app.services.v0.product_service import product_service_v0


router = APIRouter(
    prefix="/products",
    tags=["Products V0"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def list_products():
    return await product_service_v0.get_all()


@router.get(
    "/{id}",
    response_model=ProductResponse
)
async def get_product_by_id_v0(id: int):
    """Lấy thông tin chi tiết của một sản phẩm theo ID.

    Version v0 trả về dữ liệu mẫu mặc định (không truy vấn cơ sở dữ liệu).
    Được sử dụng cho mục đích testing và demo ổn định.

    **Args:**
    - `id` (int): ID của sản phẩm cần lấy thông tin (số nguyên dương)

    **Returns:**
    - ProductResponse: Đối tượng chứa thông tin chi tiết sản phẩm
      - _id: Mã định danh sản phẩm
      - product_name: Tên sản phẩm
      - age_range: Độ tuổi phù hợp
      - ingredients: Danh sách thành phần chính
      - additive: Danh sách phụ gia/chất bảo quản
      - nutrition: Thông tin dinh dưỡng
      - manufacturer: Nhà sản xuất
      - mfg_date: Ngày sản xuất
      - expiry_date: Ngày hết hạn
      - net_weight: Khối lượng ròng
      - allergen: Cảnh báo chứa chất gây dị ứng
      - warning: Hướng dẫn sử dụng/cảnh báo khác
      - origin: Xuất xứ sản phẩm
      - createdAt: Thời gian tạo (UTC)
      - timeZone: Múi giờ
      - createdAtLocal: Thời gian tạo (giờ địa phương)

    **Lưu ý:**
    - Trong v0, hàm luôn trả về dữ liệu mẫu giống nhau bất kể id là bao nhiêu
    - Để truy vấn dữ liệu thực từ database, sử dụng version v1 hoặc cao hơn
    """
    return await product_service_v0.get_by_id(product_id=id)
