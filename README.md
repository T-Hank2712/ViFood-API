# ViFood API

ViFood API là backend service cho **ViFood**, một nền tảng hỗ trợ người dùng hiểu rõ hơn về nhãn thực phẩm đóng gói. API cung cấp các chức năng xác thực người dùng, quản lý hồ sơ sức khỏe, tra cứu dữ liệu dinh dưỡng, thành phần, phụ gia thực phẩm và trích xuất thông tin sản phẩm từ hình ảnh nhãn thực phẩm bằng AI.

Project được xây dựng theo kiến trúc phân lớp rõ ràng với **FastAPI**, **Neo4j**, **JWT Authentication**, **AWS S3** và một AI extraction service bên ngoài.

## Điểm nổi bật

- Cung cấp RESTful API cho dinh dưỡng, thành phần, phụ gia, danh mục thực phẩm, mục tiêu sức khỏe và hồ sơ người dùng.
- Sử dụng Neo4j làm graph database để lưu trữ và truy vấn tri thức thực phẩm - dinh dưỡng.
- Hỗ trợ trích xuất thông tin sản phẩm từ ảnh nhãn thực phẩm thông qua AI service.
- Lưu trữ ảnh upload/scans trên AWS S3.
- Bảo vệ các API người dùng bằng JWT access token và refresh token.
- Hỗ trợ Docker Compose để chạy API và Neo4j cùng lúc.

## Công nghệ sử dụng

- **Backend:** FastAPI, Python 3.11
- **Database:** Neo4j
- **Authentication:** JWT
- **Storage:** AWS S3
- **Validation:** Pydantic
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest

## Cách khởi chạy

### 1. Cài đặt dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

Tạo file `.env` từ file mẫu:

```bash
cp .env.example .env
```

Sau đó cập nhật các giá trị cần thiết trong `.env`, đặc biệt là:

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `SECRET_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET`
- `AI_API_URL`

### 3. Chạy local

```bash
python run.py
```

Hoặc chạy bằng Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger Docs:

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

API:

```text
http://localhost:8000
```

Neo4j Browser:

```text
http://localhost:7475
```

## Nhóm API chính

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/nutrients`
- `GET /api/v1/ingredients`
- `GET /api/v1/additives`
- `GET /api/v1/search`
- `POST /api/v1/products/extract`

## Cấu trúc project

```text
app/
├── core/            # Cấu hình, kết nối database, dependencies
├── repositories/    # Tầng truy cập dữ liệu
├── services/        # Business logic
├── routers/         # API endpoints
├── schemas/         # Request và response schemas
├── models/          # Domain models
├── templates/       # Template section cho response
└── main.py          # FastAPI entry point
```

## Kiểm thử

```bash
python -m pytest -q
```
# ViFood API

ViFood API là backend service cho **ViFood**, một nền tảng hỗ trợ người dùng hiểu rõ hơn về nhãn thực phẩm đóng gói. API cung cấp các chức năng xác thực người dùng, quản lý hồ sơ sức khỏe, tra cứu dữ liệu dinh dưỡng, thành phần, phụ gia thực phẩm và trích xuất thông tin sản phẩm từ hình ảnh nhãn thực phẩm bằng AI.

Project được xây dựng theo kiến trúc phân lớp rõ ràng với **FastAPI**, **Neo4j**, **JWT Authentication**, **AWS S3** và một AI extraction service bên ngoài.

## Điểm nổi bật

- Cung cấp RESTful API cho dinh dưỡng, thành phần, phụ gia, danh mục thực phẩm, mục tiêu sức khỏe và hồ sơ người dùng.
- Sử dụng Neo4j làm graph database để lưu trữ và truy vấn tri thức thực phẩm - dinh dưỡng.
- Hỗ trợ trích xuất thông tin sản phẩm từ ảnh nhãn thực phẩm thông qua AI service.
- Lưu trữ ảnh upload/scans trên AWS S3.
- Bảo vệ các API người dùng bằng JWT access token và refresh token.
- Hỗ trợ Docker Compose để chạy API và Neo4j cùng lúc.

## Công nghệ sử dụng

- **Backend:** FastAPI, Python 3.11
- **Database:** Neo4j
- **Authentication:** JWT
- **Storage:** AWS S3
- **Validation:** Pydantic
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest

## Cách khởi chạy

### 1. Cài đặt dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Cấu hình biến môi trường

Tạo file `.env` từ file mẫu:

```bash
cp .env.example .env
```

Sau đó cập nhật các giá trị cần thiết trong `.env`, đặc biệt là:

- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `SECRET_KEY`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_S3_BUCKET`
- `AI_API_URL`

### 3. Chạy local

```bash
python run.py
```

Hoặc chạy bằng Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger Docs:

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

API:

```text
http://localhost:8000
```

Neo4j Browser:

```text
http://localhost:7475
```

## Nhóm API chính

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/nutrients`
- `GET /api/v1/ingredients`
- `GET /api/v1/additives`
- `GET /api/v1/search`
- `POST /api/v1/products/extract`

## Cấu trúc project

```text
app/
├── core/            # Cấu hình, kết nối database, dependencies
├── repositories/    # Tầng truy cập dữ liệu
├── services/        # Business logic
├── routers/         # API endpoints
├── schemas/         # Request và response schemas
├── models/          # Domain models
├── templates/       # Template section cho response
└── main.py          # FastAPI entry point
```

## Kiểm thử

```bash
python -m pytest -q
```
