from pydantic import BaseModel


class Reading(BaseModel):
    Title: str
    Body: str
