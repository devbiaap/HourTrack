from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime, timezone

from app.database.database import Base

class Justificativa(Base):
    __tablename__ = "justificativas"

    id = Column(Integer,
                primary_key=True, 
                index=True)
    usuario_id = Column(Integer,
                        nullable=False)
    data = Column(Date,
                  nullable=False)
    motivo = Column(String(500),
                    nullable=False)
    status = Column(String(50), 
                    nullable=False,
                    default="PENDENTE")
    data_criacao = Column(DateTime,
                          default=lambda: datetime.now(timezone.utc))