import os
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db
from app.schemas import ShortenUrlRequest, ShortenUrlResponse
from app.code_generator import generate_unique_code

models.Base.metadata.create_all(bind=engine)

EXPIRATION_DAYS = int(os.getenv("URL_EXPIRATION_DAYS", "30"))

app = FastAPI(
    title="URL Shortener API",
    description="Encurta URLs longas em codigos curtos com expiracao configuravel",
    version="1.0.0",
)


@app.post("/shorten-url", response_model=ShortenUrlResponse)
def shorten_url(payload: ShortenUrlRequest, request: Request, db: Session = Depends(get_db)):
    code = generate_unique_code(db)
    expires_at = datetime.now(timezone.utc) + timedelta(days=EXPIRATION_DAYS)

    entry = models.ShortenedUrl(
        short_code=code,
        original_url=str(payload.url),
        expires_at=expires_at,
    )
    db.add(entry)
    db.commit()

    base_url = str(request.base_url).rstrip("/")
    return ShortenUrlResponse(url=f"{base_url}/{code}")


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    entry = db.query(models.ShortenedUrl).filter(
        models.ShortenedUrl.short_code == short_code
    ).first()

    if entry is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    expires_at = entry.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Short URL expired")

    return RedirectResponse(url=entry.original_url)
