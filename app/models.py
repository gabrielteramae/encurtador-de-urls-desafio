from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class ShortenedUrl(Base):
    __tablename__ = "shortened_urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
