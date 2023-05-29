from pydantic import BaseSettings

class Settings(BaseSettings):
    USER: str = ''
    PASSWORD: str = ''
    DROPBOX_APP_KEY: str = ''
    DROPBOX_APP_SECRET: str = ''
    DROPBOX_REFRESH_TOKEN: str = ''
    LOCAL_DIR: str = ''
    # HOSTNAME: str = ''
    # PORT: int = 0


    class Config:
        env_file = ".env"
        
        
    def update_settings(self, new_settings: dict):
        '''Update settings.'''
        for key, value in new_settings.items():
            setattr(self, key, value)


    def save_settings(self):
        '''Save settings to file.'''
        with open('.env', 'w') as f:
            for key, value in self.dict().items():
                f.write(f'{key}={value}\n')
            f.close()


settings = Settings()
