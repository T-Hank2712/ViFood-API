"""
Application Configuration
Quản lý tất cả cấu hình của ứng dụng
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Set, Optional, Literal
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
    
    # ==================== Database Settings ====================
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str = Field(default="neo4j")
    
    kc_neo4j_uri: str
    kc_neo4j_username: str
    kc_neo4j_password: str
    kc_neo4j_database: str = Field(default="neo4j")
    
    # ==================== AWS S3 Settings ====================
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    aws_s3_bucket: str
    
    # ==================== Server Settings ====================
    host: str = "0.0.0.0"
    port: int = 8002
    
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
    ai_api_url: str
    ai_extract: str = "/extract"
    products_default_version: Literal["v0", "v1"] = "v0"
    products_canary_enabled: bool = False
    products_canary_percent: int = Field(default=0, ge=0, le=100)
    products_canary_target_version: Literal["v0", "v1"] = "v1"
    
    # ==================== Database Settings (for future) ====================
    database_url: Optional[str] = None
    
    # ==================== Security Settings ====================
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ALGORITHM: str
    
    # Pydantic v2 configuration for BaseSettings
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Tạo singleton instance của Settings
    Sử dụng lru_cache để chỉ tạo 1 instance duy nhất
    """
    return Settings()


# Export settings instance
settings = get_settings()
