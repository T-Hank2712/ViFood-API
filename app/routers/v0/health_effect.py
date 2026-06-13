# from fastapi import APIRouter, HTTPException, status
# from app.services.v0.health_effect_service import HealthEffectServiceV0

# router = APIRouter(
#     prefix="/health-effects",
#     tags=["Health Effects V0"])

# health_effect_service = HealthEffectServiceV0()


# @router.get("/")
# def list_health_effects():
#     """
#     Lấy danh sách tất cả tác động sức khỏe (Health Effect).

#     Version v0 trả về dữ liệu mẫu (mock data),
#     không truy vấn cơ sở dữ liệu.

#     **Returns:**
#     - List[HealthEffect]: Danh sách tác động sức khỏe
#       - id (int): Mã định danh tác động
#       - title (str): Tên tác động

#     **Lưu ý:**
#     - v0 sử dụng dữ liệu giả lập (mock)
#     - Không lưu trữ lâu dài
#     - Phục vụ testing/demo
#     """
#     return health_effect_service.get_all_health_effects()


# @router.get("/{id}")
# def get_health_effect_by_id(id: int):
#     """
#     Lấy thông tin chi tiết của một tác động sức khỏe theo ID.

#     **Args:**
#     - `id` (int): ID của tác động sức khỏe (số nguyên dương)

#     **Returns:**
#     - HealthEffectResponse:
#       - id (int): Mã tác động
#       - title (str): Tên tác động
#     **Lưu ý:**
#     - Nếu không tìm thấy, trả về thông báo lỗi
#     - v0 không truy vấn database thật
#     """
#     health_effect = health_effect_service.get_health_effect_by_id(id)
#     if not health_effect:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health Effect not found")
#     return health_effect


# @router.post("/")
# def create_health_effect(title: str):
#     """
#     Tạo mới một tác động sức khỏe.

#     **Args:**
#     - `title` (str): Tên tác động sức khỏe

#     **Returns:**
#     - HealthEffectResponse:
#       - id (int): Mã tác động mới
#       - title (str): Tên tác động
#     **Lưu ý:**
#     - v0 không lưu trữ lâu dài, chỉ phục vụ testing/demo
#     """
#     new_health_effect = health_effect_service.create_health_effect(title)
#     return new_health_effect


# @router.put("/{id}")
# def update_health_effect(id: int, title: str):
#     """
#     Cập nhật thông tin của một tác động sức khỏe.

#     **Args:**
#     - `id` (int): ID của tác động sức khỏe cần cập nhật
#     - `title` (str): Tên mới cho tác động sức khỏe

#     **Returns:**
#     - HealthEffectResponse:
#       - id (int): Mã tác động
#       - title (str): Tên tác động đã cập nhật
#     **Lưu ý:**
#     - Nếu không tìm thấy, trả về thông báo lỗi
#     - v0 không lưu trữ lâu dài, chỉ phục vụ testing/demo
#     """
#     updated_health_effect = health_effect_service.update_health_effect(id, title)
#     if not updated_health_effect:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health Effect not found")
#     return updated_health_effect


# @router.delete("/{id}")
# def delete_health_effect(id: int):
#     """
#     Xóa một tác động sức khỏe theo ID.

#     **Args:**
#     - `id` (int): ID của tác động sức khỏe cần xóa

#     **Returns:**
#     - dict: Thông báo kết quả xóa
#       - message (str): "Health effect deleted successfully"
#     **Lưu ý:**
#     - v0 không lưu trữ lâu dài, chỉ phục vụ testing/demo
#     - Nếu không tìm thấy, trả về thông báo lỗi
#     """
#     result = health_effect_service.delete_health_effect(id)
#     return result
