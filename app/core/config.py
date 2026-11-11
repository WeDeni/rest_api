from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str
    cors_allowed_origin: list[str]

    
def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = 'postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres',
        cors_allowed_origin = ['http://localhost:3000', 'http://localhost:8080']
    )