# from fastapi import APIRouter, HTTPException, status
# from app.services.v0.nutrient_service import NutrientServiceV0

# from app.models.food_category import FoodCategory
# from app.models.health_effect import HealthEffect

# router = APIRouter(
#     prefix="/nutrients",
#     tags=["Nutrients V0"]
# )

# nutrient_service = NutrientServiceV0()


# @router.get("/")
# def list_nutrients():
#     """
#     Lấy danh sách tất cả chất dinh dưỡng (Nutrient).

#     Version v0 trả về dữ liệu mẫu mặc định (mock data),
#     không truy vấn cơ sở dữ liệu.
#     Được sử dụng cho mục đích testing và demo.

#     **Returns:**
#     - List[Nutrient]: Danh sách các chất dinh dưỡng
#       - id (int): Mã định danh chất dinh dưỡng
#       - name (str): Tên chất dinh dưỡng
#       - description (str | None): Mô tả chất dinh dưỡng
#       - image (str | None): URL hình ảnh chất dinh dưỡng
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa chất dinh dưỡng

#     **Lưu ý:**
#     - Trong v0, dữ liệu luôn cố định (mock data)
#     - Không phụ thuộc database
#     - Không phản ánh dữ liệu thực tế
#     """
#     return nutrient_service.get_all_nutrients()


# @router.get("/{id}")
# def get_nutrient_by_id(id: int):
#     """
#     Lấy thông tin chi tiết của một chất dinh dưỡng theo ID.

#     Version v0 trả về dữ liệu mẫu mặc định.

#     **Args:**
#     - `id` (int): ID của chất dinh dưỡng cần lấy thông tin (số nguyên dương)

#     **Returns:**
#     - Nutrient: Thông tin chi tiết chất dinh dưỡng
#       - id (int): Mã chất dinh dưỡng
#       - name (str): Tên chất dinh dưỡng
#       - description (str | None): Mô tả chất dinh dưỡng
#       - image (str | None): URL hình ảnh chất dinh dưỡng
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa chất dinh dưỡng

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy chất dinh dưỡng

#     **Lưu ý:**
#     - v0 không truy vấn database thật
#     """
#     nutrient = nutrient_service.get_nutrient_by_id(id)
#     if not nutrient:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Nutrient with ID {id} not found"
#         )
#     return nutrient


# @router.post("/")
# def create_nutrient(name: str, description: str | None = None, image: str | None = None,
#                     effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
#     """
#     Tạo mới một chất dinh dưỡng.

#     Version v0 tạo mới dựa trên dữ liệu mẫu, không lưu vào database thật.

#     **Args:**
#     - `name` (str): Tên chất dinh dưỡng (bắt buộc)
#     - `description` (str | None): Mô tả chất dinh dưỡng (tùy chọn)

#     **Returns:**
#     - Nutrient: Thông tin chất dinh dưỡng vừa tạo
#       - id (int): Mã chất dinh dưỡng mới
#       - name (str): Tên chất dinh dưỡng
#       - description (str | None): Mô tả chất dinh dưỡng
#       - image (str | None): URL hình ảnh chất dinh dưỡng
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa chất dinh dưỡng

#     **Lưu ý:**
#     - v0 không lưu dữ liệu vào database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     return nutrient_service.create_nutrient(name, description, image, effects, found_in)


# @router.put("/{id}")
# def update_nutrient(id: int, name: str, description: str | None = None, image: str | None = None,
#                     effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
#     """
#     Cập nhật thông tin một chất dinh dưỡng.

#     Version v0 cập nhật dựa trên dữ liệu mẫu, không lưu vào database thật.

#     **Args:**
#     - `id` (int): ID của chất dinh dưỡng cần cập nhật (số nguyên dương)
#     - `name` (str): Tên chất dinh dưỡng mới (bắt buộc)
#     - `description` (str | None): Mô tả chất dinh dưỡng mới (tùy chọn)
#     - `image` (str | None): URL hình ảnh chất dinh dưỡng mới (tùy chọn)
#     - `effects` (List[HealthEffect] | None): Danh sách tác động sức khỏe mới (tùy chọn)
#     - `found_in` (List[FoodCategory] | None): Danh sách loại thực phẩm chứa chất dinh dưỡng mới (tùy chọn)

#     **Returns:**
#     - Nutrient: Thông tin chất dinh dưỡng sau khi cập nhật
#       - id (int): Mã chất dinh dưỡng
#       - name (str): Tên chất dinh dưỡng
#       - description (str | None): Mô tả chất dinh dưỡng
#       - image (str | None): URL hình ảnh chất dinh dưỡng
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa chất dinh dưỡng

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy chất dinh dưỡng cần cập nhật

#     **Lưu ý:**
#     - v0 không lưu dữ liệu vào database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     updated_nutrient = nutrient_service.update_nutrient(id, name, description, image, effects, found_in)
#     if not updated_nutrient:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Nutrient with ID {id} not found"
#         )
#     return updated_nutrient


# @router.delete("/{id}")
# def delete_nutrient(id: int):
#     """
#     Xóa một chất dinh dưỡng theo ID.

#     Version v0 xóa dựa trên dữ liệu mẫu, không ảnh hưởng đến database thật.

#     **Args:**
#     - `id` (int): ID của chất dinh dưỡng cần xóa (số nguyên dương)

#     **Returns:**
#     - dict: Thông báo kết quả xóa
#       - message (str): "Nutrient deleted successfully"

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy chất dinh dưỡng cần xóa

#     **Lưu ý:**
#     - v0 không xóa dữ liệu trong database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     result = nutrient_service.delete_nutrient(id)
#     if "message" not in result:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Nutrient with ID {id} not found"
#         )
#     return result
