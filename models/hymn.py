from pydantic import BaseModel


class Hymn(BaseModel):
    Number: int
    Title: str
