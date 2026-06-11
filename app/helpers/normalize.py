import unicodedata
import re


def normalize_key(text: str) -> str:
    # 1. trim + lowercase
    text = text.strip().lower()

    # 2. remove accents (tiếng Việt → không dấu)
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # 3. replace spaces -> dash
    text = re.sub(r"\s+", "-", text)

    # 4. remove special chars
    text = re.sub(r"[^a-z0-9\-]", "", text)

    # 5. remove duplicate dashes
    text = re.sub(r"-+", "-", text)

    return text
