"""
Application Configuration
Quản lý tất cả cấu hình của ứng dụng
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Set, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """
    Cấu hình ứng dụng
    Có thể override bằng biến môi trường hoặc file .env
    """
    
    # ==================== API Settings ====================
    app_name: str = "FastAPI Application"
    app_version: str = "1.0.0"
    app_description: str = "A scalable FastAPI application with modular structure"
    debug: bool = False
    
    # ==================== Server Settings ====================
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ==================== CORS Settings ====================
    allowed_origins: list = ["*"]
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]
    
    # ==================== Upload Settings ====================
    upload_dir: Path = Path("uploads")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_extensions: Set[str] = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
    
    # ==================== URL Settings ====================
    base_url: str = "http://localhost:8000"
    api_prefix: str = "/api"
    
    # ==================== Database Settings (for future) ====================
    database_url: Optional[str] = None
    
    # ==================== Security Settings ====================
    api_key: str = "your-secret-api-key-change-this"  # API Key để bảo vệ endpoints
    secret_key: Optional[str] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    """
    Tạo singleton instance của Settings
    Sử dụng lru_cache để chỉ tạo 1 instance duy nhất
    """
    return Settings()


# Export settings instance
settings = get_settings()
