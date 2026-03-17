# 🚀 Quick Start Guide

## Cài đặt nhanh

```powershell
# 1. Tạo và kích hoạt virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Cấu hình API Key (QUAN TRỌNG!)
copy .env.example .env
# Mở file .env và đổi API_KEY thành key của bạn

# 4. Chạy ứng dụng
python run.py
```

## Truy cập

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Test API

**Chỉnh API Key trong test_api.py trước:**
```python
API_KEY = "your-actual-api-key-from-env"
```

**Chạy test:**
```powershell
python test_api.py
```

## 🔐 Sử dụng API Key

Upload endpoints yêu cầu API Key trong header:

```bash
curl -X POST "http://localhost:8000/api/upload/image" \
  -H "X-API-Key: your-api-key" \
  -F "file=@image.jpg"
```

Xem chi tiết: [SECURITY.md](SECURITY.md)

## Cấu trúc quan trọng

```
app/
├── main.py              # Entry point
├── core/
│   ├── config.py       # Cấu hình
│   └── dependencies.py # Dependencies
├── routers/            # API endpoints
├── models/             # Pydantic schemas
├── services/           # Business logic
└── utils/              # Helper functions
```

## Thêm API mới

1. Tạo model trong `app/models/`
2. Tạo service trong `app/services/`
3. Tạo router trong `app/routers/`
4. Register trong `app/main.py`

## Endpoints có sẵn

- `GET /` - Root
- `GET /health` - Health check
- `GET /api/upload/config` - Upload config
- `POST /api/upload/image` - Upload image
- `DELETE /api/upload/image/{filename}` - Delete image
- `GET /api/example/` - Example endpoint
