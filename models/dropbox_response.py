from pydantic import BaseModel


class DropboxResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    uid: str
    account_id: str