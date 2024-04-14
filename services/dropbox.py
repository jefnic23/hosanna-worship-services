import webbrowser
from datetime import date

import requests
from dropbox import Dropbox as dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

from models.dropbox_response import DropboxResponse
from services.settings import Settings


class Dropbox:
    """Class for interacting with Dropbox."""

    def __init__(self, settings: Settings):
        self.day: date = date.today()
        self._path = f"{settings.LOCAL_DIR}/services"
        self._app_key: str = settings.DROPBOX_APP_KEY
        self._app_secret: str = settings.DROPBOX_APP_SECRET
        self._token: str = settings.DROPBOX_REFRESH_TOKEN
        self._dbx: dropbox

    def upload(
        self,
        filename: str,
    ) -> None:
        """Upload a file to Dropbox."""
        try:
            with open(f"{self._path}/{self.day}/{filename}", "rb") as f:
                file = f.read()

            self._dbx.files_upload(
                file, f"/{self.day}/{filename}", mode=WriteMode.overwrite
            )
        except ApiError as err:
            raise err

    def close(self) -> None:
        """Close the connection to Dropbox."""
        self._dbx.close()

    def connect(self) -> dropbox:
        """Connect to Dropbox."""
        try:
            self._dbx = dropbox(
                app_key=self._app_key,
                app_secret=self._app_secret,
                oauth2_refresh_token=self._token,
            )
        except AuthError as err:
            raise err

    def get_access_code(self) -> None:
        """Open a browser and request an access code."""
        url = (
            f"https://www.dropbox.com/oauth2/authorize?client_id={self._app_key}&"
            f"response_type=code&token_access_type=offline"
        )
        webbrowser.open_new(url)

    def get_refresh_token(self, access_code: str) -> None:
        data = f"code={access_code}&grant_type=authorization_code"

        response = requests.post(
            "https://api.dropboxapi.com/oauth2/token",
            data=data,
            auth=(self._app_key, self._app_secret),
        )

        self._token = DropboxResponse(**response.json()).refresh_token
