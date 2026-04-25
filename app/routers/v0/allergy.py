from fastapi import APIRouter, HTTPException, status
from app.services.v0.allergy_service import AllergyServiceV0

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies V0"]
)


@router.get("/")
def list_allergies():
    """
    Lấy danh sách tất cả chất gây dị ứng (Allergy).

    Version v0 trả về dữ liệu mẫu mặc định (mock data),
    không truy vấn cơ sở dữ liệu.
    Được sử dụng cho mục đích testing và demo.

    **Returns:**
    - List[Allergy]: Danh sách các chất dị ứng
      - id (int): Mã định danh chất dị ứng
      - name (str): Tên chất dị ứng

    **Lưu ý:**
    - Trong v0, dữ liệu luôn cố định (mock data)
    - Không phụ thuộc database
    - Không phản ánh dữ liệu thực tế
    """
    return AllergyServiceV0.get_all_allergies()


@router.get("/{id}")
def get_allergy_by_id(id: int):
    """
    Lấy thông tin chi tiết của một chất gây dị ứng theo ID.

    Version v0 trả về dữ liệu mẫu mặc định.

    **Args:**
    - `id` (int): ID của chất dị ứng cần lấy thông tin (số nguyên dương)

    **Returns:**
    - Allergy: Thông tin chi tiết chất dị ứng
      - id (int): Mã chất dị ứng
      - name (str): Tên chất dị ứng

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy chất dị ứng

    **Lưu ý:**
    - v0 không truy vấn database thật
    """
    allergy = AllergyServiceV0.get_allergy_by_id(id)
    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allergy with ID {id} not found"
        )
    return allergy
    

@router.post("/")
def create_allergy(name: str):
    """
    Tạo mới một chất gây dị ứng.

    Version v0 tạo dữ liệu trong bộ nhớ tạm (mock).

    **Args:**
    - `name` (str): Tên chất dị ứng

    **Returns:**
    - Allergy: Thông tin chất dị ứng vừa tạo
      - id (int): Mã chất dị ứng
      - name (str): Tên chất dị ứng

    **Lưu ý:**
    - Dữ liệu không được lưu vĩnh viễn
    - Chỉ phục vụ demo/test
    """
    return AllergyServiceV0.create_allergy(name)


@router.put("/{id}")
def update_allergy(id: int, name: str):
    """
    Cập nhật thông tin chất dị ứng theo ID.

    **Args:**
    - `id` (int): ID của chất dị ứng cần cập nhật
    - `name` (str): Tên chất dị ứng mới

    **Returns:**
    - Allergy: Thông tin chất dị ứng sau khi cập nhật
      - id (int): Mã chất dị ứng
      - name (str): Tên chất dị ứng đã cập nhật

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy chất dị ứng

    **Lưu ý:**
    - v0 chỉ cập nhật dữ liệu mock
    """
    allergy = AllergyServiceV0.update_allergy(id, name)
    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allergy with ID {id} not found"
        )
    return allergy


@router.delete("/{id}")
def delete_allergy(id: int):
    """
    Xóa một chất dị ứng theo ID.

    **Args:**
    - `id` (int): ID của chất dị ứng cần xóa
    **Returns:**
    - dict:
      - message (str): Thông báo xóa thành công

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy chất dị ứng

    **Lưu ý:**
    - v0 chỉ xóa dữ liệu trong bộ nhớ tạm
    """
    allergy = AllergyServiceV0.get_allergy_by_id(id)
    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Allergy with ID {id} not found"
        )
    return AllergyServiceV0.delete_allergy(id)
