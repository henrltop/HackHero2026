from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://vigilia:vigilia@localhost:5432/vigilia"
    SECRET_KEY: str = "hackathon-secret-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    MISTRAL_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
