from pydantic import BaseModel


class Hymn(BaseModel):
    number: int
    title: str
