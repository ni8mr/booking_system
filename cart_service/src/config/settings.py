from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@postgres:5432/sheba"
    jwt_public_key: str = "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()