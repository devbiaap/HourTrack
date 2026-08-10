from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cargo: str
    data_criacao: datetime

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    cargo: str | None = None
    