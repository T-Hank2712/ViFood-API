#!/bin/bash
# ==============================================================
# rollback.sh — Khôi phục về image trước đó
#
# Cách dùng (chạy trên VPS):
#   bash /opt/vifood/scripts/rollback.sh
#
# Script đọc .previous_image để biết image cần rollback về.
# ==============================================================

set -euo pipefail

# ---- Config ----
DEPLOY_DIR="${DEPLOY_DIR:-/opt/vifood}"
COMPOSE_FILE="$DEPLOY_DIR/docker-compose.prod.yml"
HEALTH_URL="http://localhost:${PORT:-8000}/health"
MAX_RETRIES=10
RETRY_INTERVAL=4

echo ""
echo "============================================"
echo "  ViFood Rollback"
echo "  Dir : $DEPLOY_DIR"
echo "============================================"

cd "$DEPLOY_DIR"

# ---- Đọc image cũ ----
if [ ! -f .previous_image ]; then
    echo "✗ Không tìm thấy file .previous_image"
    echo "  Không thể rollback tự động."
    echo "  Chạy thủ công: docker compose -f docker-compose.prod.yml up -d"
    exit 1
fi

PREVIOUS_IMAGE=$(cat .previous_image)

if [ -z "$PREVIOUS_IMAGE" ]; then
    echo "✗ File .previous_image rỗng. Không thể rollback."
    exit 1
fi

echo "[1/4] Rolling back to: $PREVIOUS_IMAGE"

# ---- Cập nhật .env về image cũ ----
if grep -q "^VIFOOD_IMAGE=" .env 2>/dev/null; then
    sed -i "s|^VIFOOD_IMAGE=.*|VIFOOD_IMAGE=${PREVIOUS_IMAGE}|" .env
else
    echo "VIFOOD_IMAGE=${PREVIOUS_IMAGE}" >> .env
fi
echo "[2/4] .env restored: VIFOOD_IMAGE=${PREVIOUS_IMAGE}"

# ---- Pull image cũ (phòng trường hợp Docker đã GC) ----
echo "[3/4] Pulling previous image..."
docker pull "$PREVIOUS_IMAGE" || echo "  Không pull được — thử dùng cached image..."

# ---- Restart API ----
docker compose -f "$COMPOSE_FILE" up -d --no-build api

# ---- Health check ----
echo "[4/4] Health check ($MAX_RETRIES retries x ${RETRY_INTERVAL}s)..."
for i in $(seq 1 "$MAX_RETRIES"); do
    sleep "$RETRY_INTERVAL"
    HTTP_STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "$HEALTH_URL" 2>/dev/null || echo "000")

    if [ "$HTTP_STATUS" = "200" ]; then
        echo ""
        echo "✓ Rollback successful!"
        echo "  Image : $PREVIOUS_IMAGE"
        echo "  Health: HTTP $HTTP_STATUS"
        echo "============================================"
        exit 0
    fi

    echo "  Attempt $i/$MAX_RETRIES — HTTP $HTTP_STATUS"
done

echo ""
echo "✗ Rollback cũng thất bại! Cần can thiệp thủ công."
echo ""
echo "  Kiểm tra logs:"
echo "    docker compose -f $COMPOSE_FILE logs api --tail=50"
echo ""
echo "  Xem tất cả images hiện có:"
echo "    docker images | grep vifood-api"
echo "============================================"
exit 1
