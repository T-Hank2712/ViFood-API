
from app.services.v1.health_goal_service_v1 import HealthGoalServiceV1
from app.core.database import neo4j_db

from app.schemas.profile_schema import HealthProfileRequest
from fastapi import APIRouter, HTTPException, status

router = APIRouter(
    prefix="/health-goals",
    tags=["Health Goals V1"]
)

health_goal_service = HealthGoalServiceV1(neo4j_db)


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
    """
    Tạo mới một mục tiêu sức khỏe.

    **Args:**
    - `name` (str): Tên mục tiêu sức khỏe

    **Returns:**
    - HealthGoalResponse:
      - id (int): Mã mục tiêu
      - name (str): Tên mục tiêu

    **Lưu ý:**
    - Dữ liệu được thêm vào cơ sở dữ liệu thật
    """
    try:
        health_goal = health_goal_service.get_all_health_goals()

        return {
            "message": "Get Health Goals success",
            "data": health_goal
        }
    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{id}")
def get_health_goal_by_id(id: str):
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
    try:
        health_goal = health_goal_service.get_health_goal_by_id(id)

        return {
                "message": "Get Health Goal success",
                "data": health_goal,
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/")
def create_health_goal(payload: HealthProfileRequest):
    """
    Tạo mới một mục tiêu sức khỏe.

    **Args:**
    - `name` (str): Tên mục tiêu sức khỏe

    **Returns:**
    - HealthGoalResponse:
      - id (int): Mã mục tiêu
      - name (str): Tên mục tiêu

    **Lưu ý:**
    - Dữ liệu được thêm vào cơ sở dữ liệu thật
    """
    try:
        health_goal = health_goal_service.create_health_goal(payload.name)

        return {
                "message": "Create Health Goal success",
                "data": health_goal,
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.patch("/{id}")
def update_health_goal(id: str, payload: HealthProfileRequest):
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
    try:
        health_goal = health_goal_service.update_health_goal(
            health_goal_id=id,
            name=payload.name,
        )

        return {
            "message": "Update Health Goal success",
            "data": health_goal,
        }

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.delete("/{id}")
def delete_health_goal(id: str):
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
    try:
        health_goal_service.delete_health_goal(health_goal_id=id)
        
        return {"message": "Delete Health Goal success"}

    except PermissionError as e:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
