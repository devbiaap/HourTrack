from datetime import datetime
from sqlalchemy import String, Column, Integer, DateTime

from app.database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False )
    cargo = Column(String(100), nullable=False )
    data_admissao = Column(DateTime,default=datetime.utcnow)

