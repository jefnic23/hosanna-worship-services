from datetime import date

import dropbox
from dropbox.exceptions import ApiError, AuthError

from config import settings


class Dropbox:
    '''Class for interacting with Dropbox.'''


    LOCAL_DIR = 'D:/Documents/Hosanna/services'


    def __init__(self, day: date):
        self._day: date = day
        self._app_key: str = settings.DROPBOX_APP_KEY
        self._app_secret: str = settings.DROPBOX_APP_SECRET
        self._token: str = settings.DROPBOX_REFRESH_TOKEN
        self._dbx = None

    
    def connect(self) -> None:
        '''Connect to Dropbox.'''
        try:
            self._dbx = dropbox.Dropbox(
                app_key=self._app_key, 
                app_secret=self._app_secret,
                oauth2_refresh_token=self._token
            )
        except AuthError as err:
            raise err
        
    
    def upload(
        self,
        ext: str,
        path: str = LOCAL_DIR
    ) -> None:
        '''Upload a file to Dropbox.'''
        try:
            with open(f'{path}/{self._day}/{self._day}.{ext}', 'rb') as f:
                file = f.read()

            self._dbx.files_upload(file, f'/{self._day}/{self._day}.{ext}')
        except ApiError as err:
            raise err
        

    def close(self) -> None: 
        '''Close the connection to Dropbox.'''
        self._dbx.close()
