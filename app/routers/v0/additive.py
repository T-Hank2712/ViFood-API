# from fastapi import APIRouter, HTTPException, status
# from app.models.food_category import FoodCategory
# from app.models.health_effect import HealthEffect
# from app.services.v0.additive_service import AdditiveServiceV0

# router = APIRouter(
#     prefix="/additives",
#     tags=["Additives V0"]
# )

# additive_service = AdditiveServiceV0()


# @router.get("/")
# def list_additives():
#     """
#     Lấy danh sách tất cả phụ gia (additive).

#     Version v0 trả về dữ liệu mẫu mặc định (mock data),
#     không truy vấn cơ sở dữ liệu.
#     Được sử dụng cho mục đích testing và demo.

#     **Returns:**
#     - List[Additive]: Danh sách các phụ gia
#       - id (int): Mã định danh phụ gia
#       - name (str): Tên phụ gia
#       - code (str | None): Mã phụ gia (ví dụ: E100)
#       - description (str | None): Mô tả phụ gia
#       - image (str | None): URL hình ảnh phụ gia
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa phụ gia

#     **Lưu ý:**
#     - Trong v0, dữ liệu luôn cố định (mock data)
#     - Không phụ thuộc database
#     - Không phản ánh dữ liệu thực tế
#     """
#     return additive_service.get_all_additives()


# @router.get("/{id}")
# def get_additive_by_id(id: int):
#     """
#     Lấy thông tin chi tiết của một phụ gia theo ID.

#     Version v0 trả về dữ liệu mẫu mặc định.

#     **Args:**
#     - `id` (int): ID của phụ gia cần lấy thông tin (số nguyên dương)

#     **Returns:**
#     - additive: Thông tin chi tiết phụ gia
#       - id (int): Mã định danh phụ gia
#       - name (str): Tên phụ gia
#       - code (str | None): Mã phụ gia (ví dụ: E100)
#       - description (str | None): Mô tả phụ gia
#       - image (str | None): URL hình ảnh phụ gia
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa phụ gia

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy phụ gia

#     **Lưu ý:**
#     - v0 không truy vấn database thật
#     """
#     additive = additive_service.get_additive_by_id(id)
#     if not additive:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Additive with ID {id} not found"
#         )
#     return additive


# @router.post("/")
# def create_additive(name: str, description: str | None = None, code: str | None = None, image: str | None = None,
#                     effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
#     """
#     Tạo mới một phụ gia.

#     Version v0 tạo phụ gia trong bộ nhớ tạm thời, không lưu vào database thật.

#     **Args:**
#     - `name` (str): Tên phụ gia (bắt buộc)
#     - `description` (str | None): Mô tả phụ gia (tùy chọn)

#     **Returns:**
#     - additive: Thông tin phụ gia vừa tạo
#       - id (int): Mã định danh phụ gia
#       - name (str): Tên phụ gia
#       - code (str | None): Mã phụ gia (ví dụ: E100)
#       - description (str | None): Mô tả phụ gia
#       - image (str | None): URL hình ảnh phụ gia
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa phụ gia

#     **Lưu ý:**
#     - v0 không lưu dữ liệu vào database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     return additive_service.create_additive(name, description, code, image, effects, found_in)


# @router.put("/{id}")
# def update_additive(id: int, name: str, description: str | None = None, code: str | None = None, image: str | None = None,
#                     effects: list[HealthEffect] | None = None, found_in: list[FoodCategory] | None = None):
#     """
#     Cập nhật thông tin một phụ gia.

#     Version v0 cập nhật phụ gia trong bộ nhớ tạm thời, không lưu vào database thật.

#     **Args:**
#     - `id` (int): ID của phụ gia cần cập nhật (số nguyên dương)
#     - `name` (str): Tên phụ gia mới (bắt buộc)
#     - `description` (str | None): Mô tả phụ gia mới (tùy chọn)
#     - `code` (str | None): Mã phụ gia mới (tùy chọn)
#     - `image` (str | None): URL hình ảnh phụ gia mới (tùy chọn)
#     - `effects` (List[HealthEffect] | None): Danh sách tác động sức khỏe mới (tùy chọn)
#     - `found_in` (List[FoodCategory] | None): Danh sách loại thực phẩm chứa phụ gia mới (tùy chọn)

#     **Returns:**
#     - additive: Thông tin phụ gia sau khi cập nhật
#       - id (int): Mã định danh phụ gia
#       - name (str): Tên phụ gia
#       - code (str | None): Mã phụ gia (ví dụ: E100)
#       - description (str | None): Mô tả phụ gia
#       - image (str | None): URL hình ảnh phụ gia
#       - effects (List[HealthEffect]): Các tác động sức khỏe liên quan
#       - found_in (List[FoodCategory]): Các loại thực phẩm chứa phụ gia

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy phụ gia để cập nhật

#     **Lưu ý:**
#     - v0 không lưu dữ liệu vào database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     updated_additive = additive_service.update_additive(id, name, description, code, image, effects, found_in)
#     if not updated_additive:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Additive with ID {id} not found"
#         )
#     return updated_additive


# @router.delete("/{id}")
# def delete_additive(id: int):
#     """
#     Xóa một phụ gia theo ID.

#     Version v0 xóa phụ gia trong bộ nhớ tạm thời, không xóa trong database thật.

#     **Args:**
#     - `id` (int): ID của phụ gia cần xóa (số nguyên dương)

#     **Returns:**
#     - message: Thông báo kết quả xóa
#       - message (str): "Additive deleted successfully"

#     **Raises:**
#     - HTTPException 404: Nếu không tìm thấy phụ gia để xóa

#     **Lưu ý:**
#     - v0 không xóa dữ liệu trong database thật
#     - Dữ liệu chỉ tồn tại trong bộ nhớ tạm thời của ứng dụng
#     """
#     result = additive_service.delete_additive(id)

#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Additive with ID {id} not found"
#         )

#     return {"message": "Additive deleted successfully"}
