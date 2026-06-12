from slugify import slugify


def generate_key(text: str) -> str:
    return slugify(text)
