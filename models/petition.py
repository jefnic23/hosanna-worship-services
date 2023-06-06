from pydantic import BaseModel


class Petition(BaseModel):
    call: str
    response: str
