"""
File Utilities
Các hàm tiện ích để xử lý file
"""
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Set


def generate_unique_filename(original_filename: str) -> str:
    """
    Tạo tên file duy nhất để tránh trùng lặp
    
    Format: {timestamp}_{uuid}_{original_name}
    Ví dụ: 20260310_103000_a1b2c3d4_photo.jpg
    
    Args:
        original_filename: Tên file gốc
        
    Returns:
        Tên file duy nhất
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    file_extension = Path(original_filename).suffix.lower()
    filename_without_ext = Path(original_filename).stem
    
    # Làm sạch tên file (remove special chars)
    filename_without_ext = "".join(
        c for c in filename_without_ext if c.isalnum() or c in (' ', '-', '_')
    ).strip()
    
    # Giới hạn độ dài tên file
    if len(filename_without_ext) > 50:
        filename_without_ext = filename_without_ext[:50]
    
    new_filename = f"{timestamp}_{unique_id}_{filename_without_ext}{file_extension}"
    return new_filename


def get_file_size_kb(file_path: Path) -> float:
    """
    Lấy kích thước file theo KB
    
    Args:
        file_path: Đường dẫn đến file
        
    Returns:
        Kích thước file theo KB (làm tròn 2 chữ số)
    """
    size_bytes = os.path.getsize(file_path)
    size_kb = round(size_bytes / 1024, 2)
    return size_kb


def validate_file_extension(filename: str, allowed_extensions: Set[str]) -> bool:
    """
    Kiểm tra extension của file có hợp lệ không
    
    Args:
        filename: Tên file cần kiểm tra
        allowed_extensions: Set các extension được phép (vd: {'.jpg', '.png'})
        
    Returns:
        True nếu hợp lệ, False nếu không
    """
    file_extension = Path(filename).suffix.lower()
    return file_extension in allowed_extensions


def ensure_directory_exists(directory: Path) -> None:
    """
    Đảm bảo thư mục tồn tại, tạo mới nếu chưa có
    
    Args:
        directory: Đường dẫn thư mục
    """
    directory.mkdir(parents=True, exist_ok=True)


def delete_file_safely(file_path: Path) -> bool:
    """
    Xóa file an toàn (không raise exception nếu file không tồn tại)
    
    Args:
        file_path: Đường dẫn file cần xóa
        
    Returns:
        True nếu xóa thành công, False nếu không
    """
    try:
        if file_path.exists() and file_path.is_file():
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def get_mime_type_from_extension(extension: str) -> str:
    """
    Lấy MIME type từ extension
    
    Args:
        extension: File extension (vd: '.jpg')
        
    Returns:
        MIME type string
    """
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.csv': 'text/csv',
        '.json': 'application/json',
        '.xml': 'application/xml',
    }
    return mime_types.get(extension.lower(), 'application/octet-stream')
