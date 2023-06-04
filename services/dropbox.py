from datetime import date

from dropbox import Dropbox as dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

from config import Settings


class Dropbox:
    '''Class for interacting with Dropbox.'''
    def __init__(self, settings: Settings):
        self.day: date = date.today()
        self._path = f'{settings.LOCAL_DIR}/services'
        self._app_key: str = settings.DROPBOX_APP_KEY
        self._app_secret: str = settings.DROPBOX_APP_SECRET
        self._token: str = settings.DROPBOX_REFRESH_TOKEN
        self._dbx: dropbox
            
    
    def upload(
        self,
        ext: str,
    ) -> None:
        '''Upload a file to Dropbox.'''
        try:
            with open(f'{self._path}/{self._day}/{self._day}.{ext}', 'rb') as f:
                file = f.read()

            self._dbx.files_upload(
                file, 
                f'/{self._day}/{self._day}.{ext}', 
                mode=WriteMode.overwrite
            )
        except ApiError as err:
            raise err
        

    def close(self) -> None: 
        '''Close the connection to Dropbox.'''
        self._dbx.close()
        
        
    def connect(self) -> dropbox:
        '''Connect to Dropbox.'''
        try:
            self._dbx = dropbox(
                app_key=self._app_key, 
                app_secret=self._app_secret,
                oauth2_refresh_token=self._token
            )
        except AuthError as err:
            raise err
