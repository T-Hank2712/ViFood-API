from fastapi import APIRouter, HTTPException, status
from app.models.food_category import FoodCategory
from app.models.health_effect import HealthEffect
from app.services.v0.ingredient_service import IngredientServiceV0

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients V0"]
)


@router.get("/")
def list_ingredients():
    """
    Lấy danh sách tất cả thành phần (ingredient).

    Version v0 trả về dữ liệu mẫu mặc định (mock data),
    không truy vấn cơ sở dữ liệu.
    Được sử dụng cho mục đích testing và demo.

    **Returns:**
    - List[Ingredient]: Danh sách các thành phần
      - id (int): Mã định danh thành phần
      - name (str): Tên thành phần
      - description (str | None): Mô tả thành phần
      - image (str | None): URL hình ảnh thành phần
      - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
      - found_in (List[FoodCategory]): Các loại thực phẩm chứa thành phần

    **Lưu ý:**
    - Trong v0, dữ liệu luôn cố định (mock data)
    - Không phụ thuộc database
    - Không phản ánh dữ liệu thực tế
    """
    return IngredientServiceV0.get_all_ingredients()


@router.get("/{id}")
def get_ingredient_by_id(id: int):
    """
    Lấy thông tin chi tiết của một thành phần theo ID.

    Version v0 trả về dữ liệu mẫu mặc định.

    **Args:**
    - `id` (int): ID của thành phần cần lấy thông tin (số nguyên dương)

    **Returns:**
    - ingredient: Thông tin chi tiết thành phần
      - id (int): Mã thành phần
      - name (str): Tên thành phần
      - description (str | None): Mô tả thành phần
      - image (str | None): URL hình ảnh thành phần
      - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
      - found_in (List[FoodCategory]): Các loại thực phẩm chứa thành phần

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy thành phần

    **Lưu ý:**
    - v0 không truy vấn database thật
    """
    ingredient = IngredientServiceV0.get_ingredient_by_id(id)
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with ID {id} not found"
        )
    return ingredient


@router.post("/")
def create_ingredient(name: str, description: str | None = None, image: str | None = None,
                      effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
    """
    Tạo mới một thành phần.

    Version v0 tạo mới dựa trên dữ liệu mẫu, không lưu vào database thật.

    **Args:**
    - `name` (str): Tên thành phần (bắt buộc)
    - `description` (str | None): Mô tả thành phần (tùy chọn)

    **Returns:**
    - ingredient: Thông tin thành phần vừa tạo
      - id (int): Mã thành phần mới
      - name (str): Tên thành phần
      - description (str | None): Mô tả thành phần
      - image (str | None): URL hình ảnh thành phần
      - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
      - found_in (List[FoodCategory]): Các loại thực phẩm chứa thành phần

    **Lưu ý:**
    - v0 không lưu dữ liệu vào database thật
    - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
    """
    return IngredientServiceV0.create_ingredient(name, description, image, effects, found_in)


@router.put("/{id}")
def update_ingredient(id: int, name: str, description: str | None = None, image: str | None = None,
                      effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
    """
    Cập nhật thông tin một thành phần.

    Version v0 cập nhật dựa trên dữ liệu mẫu, không lưu vào database thật.

    **Args:**
    - `id` (int): ID của thành phần cần cập nhật (số nguyên dương)
    - `name` (str): Tên thành phần mới (bắt buộc)
    - `description` (str | None): Mô tả thành phần mới (tùy chọn)
    - `image` (str | None): URL hình ảnh thành phần
    - `effects` (List[HealthEffect]): Các tác động sức khỏe liên quan
    - `found_in` (List[FoodCategory]): Các loại thực phẩm chứa thành phần

    **Returns:**
    - ingredient: Thông tin thành phần sau khi cập nhật
      - id (int): Mã thành phần
      - name (str): Tên thành phần
      - description (str | None): Mô tả thành phần
      - image (str | None): URL hình ảnh thành phần
      - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
      - found_in (List[FoodCategory]): Các loại thực phẩm chứa thành phần

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy thành phần cần cập nhật

    **Lưu ý:**
    - v0 không lưu dữ liệu vào database thật
    - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
    """
    updated_ingredient = IngredientServiceV0.update_ingredient(id, name, description, image, effects, found_in)
    if not updated_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with ID {id} not found"
        )
    return updated_ingredient


@router.delete("/{id}")
def delete_ingredient(id: int):
    """
    Xóa một thành phần theo ID.

    Version v0 xóa dựa trên dữ liệu mẫu, không ảnh hưởng đến database thật.

    **Args:**
    - `id` (int): ID của thành phần cần xóa (số nguyên dương)

    **Returns:**
    - dict: Thông báo kết quả xóa
      - message (str): "ingredient deleted successfully"

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy thành phần cần xóa

    **Lưu ý:**
    - v0 không xóa dữ liệu trong database thật
    - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
    """
    result = IngredientServiceV0.delete_ingredient(id)
    if "message" not in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ingredient with ID {id} not found"
        )
    return result
