"""
Version routing helpers
Hỗ trợ chọn version cho alias endpoint (default + canary).
"""
import hashlib


def _stable_percent(value: str) -> int:
    """
    Chuyển chuỗi thành percent ổn định trong khoảng [0, 99].
    """
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def choose_products_version(
    default_version: str,
    canary_enabled: bool,
    canary_percent: int,
    canary_target_version: str,
    key: str,
) -> str:
    """
    Chọn version cho /api/products/{id}.

    Quy tắc:
    - Nếu canary tắt hoặc canary_percent = 0 -> luôn default_version
    - Nếu canary bật -> một phần request theo key sẽ đi vào canary_target_version
    """
    if not canary_enabled or canary_percent <= 0:
        return default_version

    if _stable_percent(key) < canary_percent:
        return canary_target_version

    return default_version
