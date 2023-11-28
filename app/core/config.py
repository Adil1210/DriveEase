from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    secret_key: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
