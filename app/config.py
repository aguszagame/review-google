from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"

    class Config:
        env_file = ".env"

settings = Settings()

mail_config = ConnectionConfig(
	MAIL_USERNAME=settings.MAIL_USERNAME,
	MAIL_PASSWORD=settings.MAIL_PASSWORD,
	MAIL_FROM=settings.MAIL_FROM,
	MAIL_PORT=settings.MAIL_PORT,
	MAIL_SERVER=settings.MAIL_SERVER,
	MAIL_TLS=True,
	MAIL_SSL=False,
	USE_CREDENTIALS=True
)