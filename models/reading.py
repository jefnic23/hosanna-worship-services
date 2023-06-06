from pydantic import BaseModel


class Reading(BaseModel):
    title: str
    body: str
