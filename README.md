# ViFood API

ViFood API là backend FastAPI cho hệ thống ViFood. Project cung cấp các API để xác thực người dùng, quản lý hồ sơ sức khỏe, tra cứu dữ liệu dinh dưỡng, thành phần, phụ gia thực phẩm và trích xuất thông tin sản phẩm từ ảnh nhãn thực phẩm.

Project sử dụng Neo4j làm cơ sở dữ liệu chính, AWS S3 để lưu ảnh upload/scans và một AI service bên ngoài để extract dữ liệu sản phẩm.

## Cách khởi chạy

### 1. Cài dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env` từ file mẫu:

```bash
cp .env.example .env
```

Sau đó cập nhật các biến cần thiết như Neo4j, JWT secret, AWS S3 và AI API URL trong `.env`.

### 3. Chạy local

```bash
python run.py
```

Hoặc:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

### 4. Chạy bằng Docker Compose

```bash
docker compose up --build
```

API sẽ chạy tại:

```text
http://localhost:8000
```

Neo4j Browser:

```text
http://localhost:7475
```
