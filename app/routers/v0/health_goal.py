from fastapi import APIRouter
from app.services.v0.health_goal_service import HealthGoalServiceV0

router = APIRouter(
    prefix="/health-goals",
    tags=["Health Goals V0"]
)

health_goal_service = HealthGoalServiceV0()


@router.get("/")
def list_health_goals():
    """
    Lấy danh sách tất cả mục tiêu sức khỏe (Health Goal).

    Version v0 trả về dữ liệu mẫu (mock data),
    không truy vấn cơ sở dữ liệu.

    **Returns:**
    - List[HealthGoal]: Danh sách mục tiêu sức khỏe
      - id (int): Mã định danh mục tiêu
      - name (str): Tên mục tiêu sức khỏe

    **Lưu ý:**
    - v0 sử dụng dữ liệu giả lập (mock)
    - Không lưu trữ lâu dài
    - Phục vụ testing/demo
    """
    return health_goal_service.get_all_health_goals()


@router.get("/{id}")
def get_health_goal_by_id(id: int):
    """
    Lấy thông tin chi tiết của một mục tiêu sức khỏe theo ID.

    **Args:**
    - `id` (int): ID của mục tiêu sức khỏe (số nguyên dương)

    **Returns:**
    - HealthGoalResponse:
      - id (int): Mã mục tiêu
      - name (str): Tên mục tiêu

    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 không truy vấn database thật
    """
    health_goal = health_goal_service.get_health_goal_by_id(id)
    return health_goal or {"error": "Health Goal not found"}


@router.post("/")
def create_health_goal(name: str):
    """
    Tạo mới một mục tiêu sức khỏe.

    **Args:**
    - `name` (str): Tên mục tiêu sức khỏe

    **Returns:**
    - HealthGoalResponse:
      - id (int): Mã mục tiêu
      - name (str): Tên mục tiêu

    **Lưu ý:**
    - Dữ liệu chỉ tồn tại trong bộ nhớ tạm (mock)
    - Không lưu vĩnh viễn
    """
    new_health_goal = health_goal_service.create_health_goal(name)
    return new_health_goal


@router.put("/{id}")
def update_health_goal(id: int, name: str):
    """
    Cập nhật thông tin mục tiêu sức khỏe theo ID.

    **Args:**
    - `id` (int): ID của mục tiêu cần cập nhật
    - `name` (str): Tên mới của mục tiêu

    **Returns:**
    - HealthGoalResponse:
      - id (int): Mã mục tiêu
      - name (str): Tên sau khi cập nhật

    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 chỉ cập nhật dữ liệu mock
    """
    updated_health_goal = health_goal_service.update_health_goal(id, name)
    return updated_health_goal or {"error": "Health Goal not found"}


@router.delete("/{id}")
def delete_health_goal(id: int):
    """
    Xóa một mục tiêu sức khỏe theo ID.

    **Args:**
    - `id` (int): ID của mục tiêu cần xóa

    **Returns:**
    - dict:
      - message (str): Thông báo kết quả

    **Lưu ý:**
    - Nếu không tìm thấy, trả về thông báo lỗi
    - v0 chỉ xóa dữ liệu trong bộ nhớ tạm
    """
    result = health_goal_service.delete_health_goal(id)
    return result or {"error": "Health Goal not found"}
