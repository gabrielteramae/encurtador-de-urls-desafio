from pydantic import BaseModel, HttpUrl, field_validator


class ShortenUrlRequest(BaseModel):
    url: HttpUrl

    @field_validator("url")
    @classmethod
    def url_curta(cls, value):
        if len(str(value)) > 2048:
            raise ValueError("URL muito longa")
        if value.username or value.password:
            raise ValueError("URL não pode ter usuário ou senha")
        return value


class ShortenUrlResponse(BaseModel):
    url: str
