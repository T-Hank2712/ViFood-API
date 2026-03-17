# 🔐 Bảo mật API

## API Key Authentication

API upload được bảo vệ bằng **API Key** để tránh bị cào (scraping) hoặc lạm dụng.

### 🔑 Cấu hình API Key

**1. Tạo file `.env` từ template:**
```powershell
copy .env.example .env
```

**2. Mở file `.env` và đổi API Key:**
```env
# Đổi key này thành một chuỗi random, phức tạp
API_KEY=abc123xyz789-your-secret-key-here
```

**💡 Gợi ý tạo API Key ngẫu nhiên:**

```powershell
# PowerShell
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString())) + [System.Guid]::NewGuid().ToString()
```

hoặc

```python
# Python
import secrets
print(secrets.token_urlsafe(32))
```

### 📤 Sử dụng API với API Key

#### cURL

```bash
curl -X POST "http://localhost:8000/api/upload/image" \
  -H "X-API-Key: your-secret-api-key-change-this" \
  -F "file=@image.jpg"
```

#### Python (requests)

```python
import requests

url = "http://localhost:8000/api/upload/image"
headers = {
    "X-API-Key": "your-secret-api-key-change-this"
}
files = {'file': open('image.jpg', 'rb')}

response = requests.post(url, files=files, headers=headers)
print(response.json())
```

#### JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/upload/image', {
  method: 'POST',
  headers: {
    'X-API-Key': 'your-secret-api-key-change-this'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

#### Postman

1. Chọn request
2. Vào tab **Headers**
3. Thêm header:
   - **Key**: `X-API-Key`
   - **Value**: `your-secret-api-key-change-this`

### 🚫 Response khi thiếu hoặc sai API Key

**Thiếu API Key (401):**
```json
{
  "detail": "Missing API Key. Please provide X-API-Key header"
}
```

**Sai API Key (403):**
```json
{
  "detail": "Invalid API Key"
}
```

### 🔒 Endpoints được bảo vệ

| Endpoint | Method | Yêu cầu API Key |
|----------|--------|-----------------|
| `/api/upload/image` | POST | ✅ Có |
| `/api/upload/image/{filename}` | DELETE | ✅ Có |
| `/api/upload/config` | GET | ❌ Không |
| `/health` | GET | ❌ Không |
| `/` | GET | ❌ Không |

### ⚙️ Tùy chỉnh

**Muốn bảo vệ thêm endpoints khác:**

```python
# app/routers/your_router.py
from app.core.dependencies import verify_api_key

@router.get("/protected")
async def protected_endpoint(api_key: str = Depends(verify_api_key)):
    return {"message": "This is protected"}
```

### 📋 Checklist Production

- [ ] Đổi API Key thành chuỗi phức tạp, không đoán được
- [ ] Không commit file `.env` vào git
- [ ] Lưu API Key ở nơi an toàn
- [ ] Rotate (đổi) API Key thường xuyên
- [ ] Monitor usage để phát hiện lạm dụng
- [ ] Cân nhắc thêm rate limiting
- [ ] Sử dụng HTTPS trong production
- [ ] Có thể dùng multiple API keys cho các clients khác nhau

### 🔄 Nâng cấp trong tương lai

Có thể mở rộng thành:
- ✨ JWT authentication với user accounts
- ✨ OAuth2 integration
- ✨ Multiple API keys với roles khác nhau
- ✨ API key có expiration time
- ✨ Rate limiting per API key
- ✨ Usage tracking & analytics

### 📚 Test với API Key

Chỉnh sửa `API_KEY` trong `test_api.py` để match với `.env`:

```python
API_KEY = "your-secret-api-key-change-this"
```

Sau đó chạy:
```powershell
python test_api.py
```

---

**⚠️ LƯU Ý QUAN TRỌNG:**
- **KHÔNG** share API key công khai
- **KHÔNG** commit `.env` vào git
- **PHẢI** đổi API key mặc định trước khi deploy
