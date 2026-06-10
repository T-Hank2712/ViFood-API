from datetime import datetime, timedelta, timezone

VN_TZ = timezone(timedelta(hours=7))


def to_iso(value):
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def to_vn_time(dt):
    if dt is None:
        return None

    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)

    return dt.astimezone(VN_TZ)
