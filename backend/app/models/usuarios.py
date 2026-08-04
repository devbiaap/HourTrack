from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False )
    cargo: Mapped[str] = mapped_column(String(50), nullable=False )
    data_admissao: Mapped[date] = mapped_column(nullable=False)

