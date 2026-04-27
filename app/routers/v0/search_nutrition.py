from fastapi import APIRouter, HTTPException, status
from app.services.v0.search_nutrition_service import SearchNutritionServiceV0

router = APIRouter(
    prefix="/search-nutrition",
    tags=["Search Nutrition V0"]
)


@router.get("/", summary="Lấy danh sách chất dinh dưỡng, thành phần, phụ gia")
def get_nutritions():
    """
    Lấy danh sách toàn bộ chất dinh dưỡng, thành phần, phụ gia.

    Version v0 trả về dữ liệu mẫu mặc định (mock data),
    không truy vấn cơ sở dữ liệu.
    Được sử dụng cho mục đích testing và demo.

    **Returns:**
    - List[searchDTO]: Danh sách kết quả tìm kiếm
      - id (int): Mã định danh
      - name (str): Tên chất dinh dưỡng/thành phần/phụ gia
      - description (str | None): Mô tả chi tiết
      - image (str | None): URL hình ảnh
      - effects (List[str]): Các tác động sức khỏe liên quan
      - found_in (List[str]): Các loại thực phẩm chứa chất dinh dưỡng/thành phần/phụ gia
      - type (str): Loại đối tượng ("nutrient", "ingredient", "additive")

    **Lưu ý:**
    - Trong v0, dữ liệu luôn cố định (mock data)
    - Không phụ thuộc database
    - Không phản ánh dữ liệu thực tế
    """
    return SearchNutritionServiceV0.get_all_nutrition()


@router.get("/{nutrition_id}", summary="Lấy thông tin chi tiết chất dinh dưỡng, thành phần, phụ gia theo ID")
def get_nutrition_by_id(nutrition_id: str):
    """
    Lấy thông tin chi tiết về một chất dinh dưỡng, thành phần, hoặc phụ gia theo ID.

    Version v0 trả về dữ liệu mẫu mặc định (mock data),
    không truy vấn cơ sở dữ liệu.
    Được sử dụng cho mục đích testing và demo.

    **Path Parameters:**
    - nutrition_id (str): ID của chất dinh dưỡng/thành phần/phụ gia theo định dạng "{type}-{id}"
      - type: "nutrient", "ingredient", hoặc "additive"
      - id: số nguyên đại diện cho ID trong mock data

    **Returns:**
    - searchDTO: Thông tin chi tiết về chất dinh dưỡng/thành phần/phụ gia
      - id (str): Mã định danh
      - name (str): Tên chất dinh dưỡng/thành phần/phụ gia
      - description (str | None): Mô tả chi tiết
      - image (str | None): URL hình ảnh
      - effects (List[str]): Các tác động sức khỏe liên quan
      - found_in (List[str]): Các loại thực phẩm chứa chất dinh dưỡng/thành phần/phụ gia
      - type (str): Loại đối tượng ("nutrient", "ingredient", "additive")

    **Lưu ý:**
    - Trong v0, dữ liệu luôn cố định (mock data)
    - Không phụ thuộc database
    - Không phản ánh dữ liệu thực tế
    """
    result = SearchNutritionServiceV0.get_nutrition_by_id(nutrition_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition not found")
    return result
