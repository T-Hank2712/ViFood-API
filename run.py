"""
Quick start script
Chạy file này để khởi động ứng dụng nhanh chóng
"""
import uvicorn
from app.core.config import settings


if __name__ == "__main__":
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📝 API Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"📖 ReDoc: http://{settings.host}:{settings.port}/redoc")
    print(f"🔧 API Prefix: {settings.api_prefix}")
    print("\nPress CTRL+C to quit\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
