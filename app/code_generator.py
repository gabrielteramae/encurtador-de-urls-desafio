import random
import string
from sqlalchemy.orm import Session
from app.models import ShortenedUrl

ALPHABET = string.ascii_letters + string.digits
MIN_LENGTH = 5
MAX_LENGTH = 10
DEFAULT_LENGTH = 6


def _random_code(length: int) -> str:
    return "".join(random.choices(ALPHABET, k=length))


def generate_unique_code(db: Session, length: int = DEFAULT_LENGTH, max_attempts: int = 10) -> str:
    if not (MIN_LENGTH <= length <= MAX_LENGTH):
        raise ValueError(f"length must be between {MIN_LENGTH} and {MAX_LENGTH}")

    for _ in range(max_attempts):
        code = _random_code(length)
        exists = db.query(ShortenedUrl).filter(ShortenedUrl.short_code == code).first()
        if not exists:
            return code

    raise RuntimeError("Could not generate a unique short code, try again")
