import ulid


def generate_id() -> str:
    return str(ulid.new())
