from datetime import date, time
from pydantic import BaseModel

class PontoCreate(BaseModel):
    data: date
    entrada: time
    saida_almoco: time | None = None
    volta_almoco: time | None = None
    saida : time | None = None
    observacao: str | None = None
    