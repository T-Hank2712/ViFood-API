#!/bin/bash
# ==============================================================
# deploy.sh — Triển khai image mới lên VPS
#
# Cách dùng:
#   bash scripts/deploy.sh <image_tag> <docker_username>
#
# VD:
#   bash scripts/deploy.sh sha-a1b2c3d myusername
#
# Script tự động rollback nếu health check thất bại.
# ==============================================================

set -euo pipefail

# ---- Arguments ----
IMAGE_TAG="${1:?Thiếu image_tag. VD: sha-a1b2c3d}"
DOCKER_USERNAME="${2:?Thiếu docker_username. VD: myusername}"

# ---- Config ----
DEPLOY_DIR="${DEPLOY_DIR:-/opt/vifood}"
COMPOSE_FILE="$DEPLOY_DIR/docker-compose.prod.yml"
FULL_IMAGE="${DOCKER_USERNAME}/vifood-api:${IMAGE_TAG}"
# Health check chạy bên trong container (tránh phụ thuộc vào port mapping của host)
HEALTH_CONTAINER="vifood-api"
MAX_RETRIES=15
RETRY_INTERVAL=4    # seconds — tổng timeout = 15 * 4 = 60s

echo ""
echo "============================================"
echo "  ViFood Deploy"
echo "  Image : $FULL_IMAGE"
echo "  Dir   : $DEPLOY_DIR"
echo "============================================"

cd "$DEPLOY_DIR"

# ---- Lưu tag hiện tại để rollback ----
CURRENT_IMAGE=$(grep "^VIFOOD_IMAGE=" .env 2>/dev/null | cut -d'=' -f2 || echo "${DOCKER_USERNAME}/vifood-api:latest")
echo "$CURRENT_IMAGE" > .previous_image
echo "[1/5] Previous image saved: $CURRENT_IMAGE"

# ---- Cập nhật VIFOOD_IMAGE trong .env ----
if grep -q "^VIFOOD_IMAGE=" .env 2>/dev/null; then
    sed -i "s|^VIFOOD_IMAGE=.*|VIFOOD_IMAGE=${FULL_IMAGE}|" .env
else
    echo "VIFOOD_IMAGE=${FULL_IMAGE}" >> .env
fi

# Đảm bảo DOCKER_USERNAME có trong .env (dùng bởi compose nếu cần)
if grep -q "^DOCKER_USERNAME=" .env 2>/dev/null; then
    sed -i "s|^DOCKER_USERNAME=.*|DOCKER_USERNAME=${DOCKER_USERNAME}|" .env
else
    echo "DOCKER_USERNAME=${DOCKER_USERNAME}" >> .env
fi
echo "[2/5] .env updated: VIFOOD_IMAGE=${FULL_IMAGE}"

# ---- Pull image mới từ Docker Hub ----
echo "[3/5] Pulling image from Docker Hub..."
docker pull "$FULL_IMAGE"

# ---- Restart services (giữ Neo4j đang chạy, không restart DB) ----
echo "[4/5] Restarting services..."
docker compose -f "$COMPOSE_FILE" up -d --no-build --no-recreate neo4j
docker compose -f "$COMPOSE_FILE" up -d --no-build api
docker compose -f "$COMPOSE_FILE" up -d --no-build nginx

# ---- Health check ----
echo "[5/5] Health check ($MAX_RETRIES retries x ${RETRY_INTERVAL}s)..."
for i in $(seq 1 "$MAX_RETRIES"); do
    sleep "$RETRY_INTERVAL"
    # Chạy curl bên trong container — không cần port expose ra host
    HTTP_STATUS=$(docker exec "$HEALTH_CONTAINER" \
        curl -sf -o /dev/null -w "%{http_code}" \
        http://localhost:8000/health 2>/dev/null || echo "000")

    if [ "$HTTP_STATUS" = "200" ]; then
        echo ""
        echo "✓ Deploy successful!"
        echo "  Image : $FULL_IMAGE"
        echo "  Health: HTTP $HTTP_STATUS"
        echo "============================================"
        exit 0
    fi

    echo "  Attempt $i/$MAX_RETRIES — HTTP $HTTP_STATUS"
done

# ---- Health check thất bại → Rollback tự động ----
echo ""
echo "✗ Health check failed after ${MAX_RETRIES} attempts!"
echo "  Initiating automatic rollback..."
echo ""

bash "$DEPLOY_DIR/scripts/rollback.sh"

# Thoát với lỗi để GitHub Actions biết deploy thất bại
exit 1
