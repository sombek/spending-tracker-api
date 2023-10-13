from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_CONNECTION: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/all-track-db"
    )
    auth0_domain: str = "dev-bmbazij1sjiidmnc.us.auth0.com"
    auth0_audience: str = "https://hello-world.example.com"


settings: Settings = Settings()
