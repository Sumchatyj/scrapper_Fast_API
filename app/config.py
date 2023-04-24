from pydantic import BaseSettings
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    db_drivername: str
    db_name: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: int

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_default_vhost: str

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
