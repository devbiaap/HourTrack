from datetime import date
from pydantic import BaseModel

class JustificativaCreate(BaseModel):
    data: date
    motivo: str