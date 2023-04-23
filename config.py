from pydantic import BaseSettings


class Settings(BaseSettings):
    USER: str
    PASSWORD: str
    DROPBOX_APP_KEY: str
    DROPBOX_APP_SECRET: str
    DROPBOX_REFRESH_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
