# ==============================================================
# Stage 1: Builder — cài dependencies vào virtual environment
# ==============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Cài hệ thống dependencies tối thiểu cần thiết để build các C extension
# (cffi, cryptography, uvloop...)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Tạo virtualenv riêng để copy sang stage production
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements trước — tận dụng Docker layer cache:
# nếu requirements.txt không đổi, bước pip install sẽ được cache lại
COPY requirements.txt .

# Upgrade pip + cài gunicorn (production process manager) + tất cả dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir gunicorn==21.2.0 \
    && pip install --no-cache-dir -r requirements.txt


# ==============================================================
# Stage 2: Production image — chỉ giữ những gì cần thiết
# ==============================================================
FROM python:3.11-slim AS production

# Metadata
LABEL maintainer="ViFood API"
LABEL version="1.0"

# Biến môi trường hệ thống
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    # Chỉ định port mặc định (có thể override qua docker run -e PORT=...)
    PORT=8000

WORKDIR /app

# Chỉ cài runtime libs (không cần build tools ở production)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # libpq-dev nếu sau này thêm PostgreSQL
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv từ builder stage
COPY --from=builder /opt/venv /opt/venv

# Tạo user không phải root để chạy app (bảo mật)
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

# Tạo thư mục uploads và phân quyền
RUN mkdir -p /app/uploads && chown -R appuser:appgroup /app

# Copy source code (sau khi copy deps để tận dụng cache)
COPY --chown=appuser:appgroup . .

# Chuyển sang non-root user
USER appuser

# Expose port
EXPOSE 8000

# Healthcheck: kiểm tra API có phản hồi không
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Production: gunicorn quản lý process, uvicorn làm worker
# --workers: số worker processes (2 * CPU + 1 là công thức chuẩn)
# --worker-class: dùng uvicorn ASGI worker
# --bind: lắng nghe trên tất cả interfaces
CMD ["gunicorn", "app.main:app", \
    "--workers", "4", \
    "--worker-class", "uvicorn.workers.UvicornWorker", \
    "--bind", "0.0.0.0:8000", \
    "--timeout", "120", \
    "--keep-alive", "5", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]
