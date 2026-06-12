"""
FastAPI Application Entry Point
Main file khởi tạo và cấu hình ứng dụng
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.core.config import settings
from app.models.base import HealthCheckResponse
from app.utils.file_utils import ensure_directory_exists

from app.core.database import neo4j_db

from app.db import db
from app.db.seed import seed

# Import routers
from app.routers import upload, example
# from app.routers.products_alias import router as products_alias_router
from app.routers.v0.product import router as product_v0_router
# from app.routers.v1.products import router as products_v1_router
# from app.routers.v0.disease import router as disease_v0_router
# from app.routers.v0.health_goal import router as health_goal_v0_router
from app.routers.v0.allergy import router as allergy_v0_router
from app.routers.v0.nutrient import router as nutrient_v0_router
from app.routers.v0.ingredient import router as ingredient_v0_router
from app.routers.v0.additive import router as additive_v0_router
from app.routers.v0.health_effect import router as health_effect_v0_router
from app.routers.v0.food_category import router as food_category_v0_router
from app.routers.v0.search_nutrition import router as search_nutrition_v0_router
# from app.routers.v0.user_profile import router as user_profile_v0_router
# from app.routers.v0.auth import router as auth_v0_router

# V1
from app.routers.v1.auth import router as auth_v1_router
from app.routers.v1.user_profile_v1 import router as profile_v1_router
from app.routers.v1.health_goal_v1 import router as health_goal_v1_router
from app.routers.v1.disease_v1 import router as disease_v1_router


# Tạo FastAPI app instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ==================== Middleware Configuration ====================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)


# ==================== Static Files ====================

# Đảm bảo upload directory tồn tại
ensure_directory_exists(settings.upload_dir)

# Mount static files (uploads)
app.mount("/uploads", StaticFiles(directory=str(settings.upload_dir)), name="uploads")


# ==================== API Routers ====================

# Include routers với prefix /api
app.include_router(upload.router, prefix=settings.api_prefix)
app.include_router(example.router, prefix=settings.api_prefix)

# Products versioning strategy:
# - /api/v0/products/{id}: luôn trỏ về v0
# - /api/v1/products/{id}: luôn trỏ về v1
# - /api/products/{id}: alias theo settings.products_default_version (+ canary)
app.include_router(product_v0_router, prefix=f"{settings.api_prefix}/v0")
# app.include_router(products_v1_router, prefix=f"{settings.api_prefix}/v1")
# app.include_router(products_alias_router, prefix=settings.api_prefix)

# TODO: Thêm các router khác ở đây
# app.include_router(users.router, prefix=settings.api_prefix)
# app.include_router(auth.router, prefix=settings.api_prefix)
# app.include_router(products.router, prefix=settings.api_prefix)

# Disease router (v0)
# app.include_router(disease_v0_router, prefix=f"{settings.api_prefix}/v0")

# Health Goal router (v0)
# app.include_router(health_goal_v0_router, prefix=f"{settings.api_prefix}/v0")

# Allergy router (v0)
app.include_router(allergy_v0_router, prefix=f"{settings.api_prefix}/v0")

# Nutrient router (v0)
app.include_router(nutrient_v0_router, prefix=f"{settings.api_prefix}/v0")

# Ingredient router (v0)
app.include_router(ingredient_v0_router, prefix=f"{settings.api_prefix}/v0")

# Additive router (v0)
app.include_router(additive_v0_router, prefix=f"{settings.api_prefix}/v0")

# Health Effect router (v0)
app.include_router(health_effect_v0_router, prefix=f"{settings.api_prefix}/v0")

# Food Category router (v0)
app.include_router(food_category_v0_router, prefix=f"{settings.api_prefix}/v0")

# Search Nutrition router (v0)
app.include_router(search_nutrition_v0_router, prefix=f"{settings.api_prefix}/v0")

# User Profile router (v0)
# app.include_router(user_profile_v0_router, prefix=f"{settings.api_prefix}/v0")

# Auth router (v0)
# app.include_router(auth_v0_router, prefix=f"{settings.api_prefix}/v0")

# ==================== V1  ====================

app.include_router(auth_v1_router, prefix=f"{settings.api_prefix}/v1")

app.include_router(profile_v1_router, prefix=f"{settings.api_prefix}/v1")

app.include_router(health_goal_v1_router, prefix=f"{settings.api_prefix}/v1")

app.include_router(disease_v1_router, prefix=f"{settings.api_prefix}/v1")


# ==================== Root Endpoints ====================

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Endpoint gốc, hiển thị thông tin API"
)
async def root():
    """Root endpoint - thông tin cơ bản về API"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.api_prefix,
        "products_default_version": settings.products_default_version,
        "products_canary_enabled": settings.products_canary_enabled,
        "products_canary_percent": settings.products_canary_percent,
        "products_canary_target_version": settings.products_canary_target_version,
        "available_endpoints": {
            "health": "/health",
            "upload": f"{settings.api_prefix}/upload",
            "example": f"{settings.api_prefix}/example",
            "products_default": f"{settings.api_prefix}/products/{{id}}",
            "products_v0": f"{settings.api_prefix}/v0/products/{{id}}",
            "products_v1": f"{settings.api_prefix}/v1/products/{{id}}"
        }
        
    }


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Health"],
    summary="Health check",
    description="Kiểm tra trạng thái hoạt động của API"
)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version
    )


@app.get("/database-test")
async def database_test():
    """Endpoint test kết nối database"""
    try:
        with neo4j_db.get_session() as session:
            result = session.run("RETURN 1 AS number")
            return {"status": "success", "data": result.data()}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """
    Chạy khi application khởi động
    Có thể thêm logic như:
    - Kết nối database
    - Khởi tạo cache
    - Load models
    - etc.
    """
    seed(db)  # Seed dữ liệu giả định vào database
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    print(f"📝 Docs: http://{settings.host}:{settings.port}/docs")
    print(f"🔧 API Prefix: {settings.api_prefix}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Chạy khi application tắt
    Có thể thêm cleanup logic
    """
    print(f"👋 Shutting down {settings.app_name}")


# ==================== Run Application ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
