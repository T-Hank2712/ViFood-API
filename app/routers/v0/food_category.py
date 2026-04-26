from fastapi import APIRouter, HTTPException, status
from app.services.v0.food_category_service import FoodCategoryServiceV0

router = APIRouter(
    prefix="/food-categories",
    tags=["Food Categories V0"])


@router.get("/")
def list_food_categories():
    """
    Lấy danh sách tất cả nhóm thực phẩm (Food Category).

    Version v0 trả về dữ liệu mẫu (mock data),
    không truy vấn cơ sở dữ liệu.

    **Returns:**
    - List[FoodCategory]: Danh sách nhóm thực phẩm
      - id (int): Mã định danh nhóm
      - name (str): Tên nhóm

    **Lưu ý:**
    - v0 sử dụng dữ liệu giả lập (mock)
    - Không lưu trữ lâu dài
    - Phục vụ testing/demo
    """
    return FoodCategoryServiceV0.get_all_food_categories()


@router.get("/{id}")
def get_food_category_by_id(id: int):
    """
    Lấy thông tin chi tiết của một nhóm thực phẩm theo ID.

    **Args:**
    - `id` (int): ID của nhóm thực phẩm (số nguyên dương)

    **Returns:**
    - FoodCategory:
      - id (int): Mã nhóm
      - name (str): Tên nhóm
    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 không truy vấn database thật
    """
    food_category = FoodCategoryServiceV0.get_food_category_by_id(id)
    if not food_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food Category not found")
    return food_category


@router.post("/")
def create_food_category(name: str):
    """
    Tạo mới một nhóm thực phẩm.

    **Args:**
    - `name` (str): Tên nhóm thực phẩm

    **Returns:**
    - FoodCategory:
      - id (int): Mã nhóm mới
      - name (str): Tên nhóm mới
    **Lưu ý:**
    - v0 không lưu trữ lâu dài, chỉ phục vụ testing/demo
    """
    return FoodCategoryServiceV0.create_food_category(name)


@router.put("/{id}")
def update_food_category(id: int, name: str):
    """
    Cập nhật thông tin của một nhóm thực phẩm.

    **Args:**
    - `id` (int): ID của nhóm thực phẩm cần cập nhật
    - `name` (str): Tên mới cho nhóm thực phẩm

    **Returns:**
    - FoodCategory:
      - id (int): Mã nhóm
      - name (str): Tên nhóm đã cập nhật
    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 không truy vấn database thật
    """
    updated_food_category = FoodCategoryServiceV0.update_food_category(id, name)
    if not updated_food_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food Category not found")
    return updated_food_category


@router.delete("/{id}")
def delete_food_category(id: int):
    """
    Xóa một nhóm thực phẩm theo ID.

    **Args:**
    - `id` (int): ID của nhóm thực phẩm cần xóa

    **Returns:**
    - dict: Thông báo kết quả xóa
      - message (str): "Food category deleted successfully"
    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 không truy vấn database thật, chỉ phục vụ testing/demo
    """
    food_category = FoodCategoryServiceV0.get_food_category_by_id(id)
    if not food_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food Category not found")
    return FoodCategoryServiceV0.delete_food_category(id)
