from pydantic import BaseModel


class Hymn(BaseModel):
    title: str
    number: str
