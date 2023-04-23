from pydantic import BaseSettings


class Settings(BaseSettings):
    USER: str
    PASSWORD: str
    DROPBOX_ACCESS_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
