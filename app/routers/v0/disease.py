from fastapi import APIRouter, HTTPException, status
from app.services.v0.disease_service import DiseaseServiceV0

router = APIRouter(
    prefix="/diseases",
    tags=["Diseases V0"]
)


@router.get("/")
def list_diseases():
    """
    Lấy danh sách tất cả bệnh (Disease).

    Version v0 trả về dữ liệu mẫu mặc định (mock data),
    không truy vấn cơ sở dữ liệu.
    Được sử dụng cho mục đích testing và demo.

    **Returns:**
    - List[DiseaseResponse]: Danh sách các bệnh
      - id (int): Mã định danh bệnh
      - name (str): Tên bệnh
      - description (str): Mô tả bệnh (nếu có)
      - createdAt (datetime): Thời gian tạo (UTC)

    **Lưu ý:**
    - Trong v0, dữ liệu luôn cố định (mock data)
    - Không phụ thuộc database
    - Không phản ánh dữ liệu thực tế
    """
    return DiseaseServiceV0.get_all()


@router.get("/{id}")
def get_disease_by_id(id: int):
    """
    Lấy thông tin chi tiết của một bệnh theo ID.

    Version v0 trả về dữ liệu mẫu mặc định.

    **Args:**
    - `id` (int): ID của bệnh cần lấy thông tin (số nguyên dương)

    **Returns:**
    - DiseaseResponse: Thông tin chi tiết bệnh
      - id (int): Mã bệnh
      - name (str): Tên bệnh
      - description (str): Mô tả bệnh
      - createdAt (datetime): Thời gian tạo

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy bệnh

    **Lưu ý:**
    - v0 không truy vấn database thật
    """
    disease = DiseaseServiceV0.get_by_id(id)

    if not disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )

    return disease


@router.post("/")
def create_disease(name: str):
    """
    Tạo mới một bệnh.

    Version v0 tạo dữ liệu trong bộ nhớ tạm (mock).

    **Args:**
    - `name` (str): Tên bệnh

    **Returns:**
    - DiseaseResponse: Thông tin bệnh vừa tạo
      - id (int): Mã bệnh
      - name (str): Tên bệnh

    **Lưu ý:**
    - Dữ liệu không được lưu vĩnh viễn
    - Chỉ phục vụ demo/test
    """
    return DiseaseServiceV0.create_disease(name)


@router.put("/{id}")
def update_disease(id: int, name: str):
    """
    Cập nhật thông tin bệnh theo ID.

    **Args:**
    - `id` (int): ID của bệnh cần cập nhật
    - `name` (str): Tên bệnh mới

    **Returns:**
    - DiseaseResponse: Thông tin bệnh sau khi cập nhật
      - id (int): Mã bệnh
      - name (str): Tên bệnh đã cập nhật

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy bệnh

    **Lưu ý:**
    - v0 chỉ cập nhật dữ liệu mock
    """
    updated_disease = DiseaseServiceV0.update_disease(id, name)

    if not updated_disease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )

    return updated_disease


@router.delete("/{id}")
def delete_disease(id: int):
    """
    Xóa một bệnh theo ID.

    **Args:**
    - `id` (int): ID của bệnh cần xóa

    **Returns:**
    - dict:
      - message (str): Thông báo xóa thành công

    **Raises:**
    - HTTPException 404: Nếu không tìm thấy bệnh

    **Lưu ý:**
    - v0 chỉ xóa dữ liệu trong bộ nhớ tạm
    """
    result = DiseaseServiceV0.delete_disease(id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disease not found"
        )

    return {"message": "Deleted successfully"}
