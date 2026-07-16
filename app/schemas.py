from pydantic import BaseModel, HttpUrl


class ShortenUrlRequest(BaseModel):
    url: HttpUrl


class ShortenUrlResponse(BaseModel):
    url: str
