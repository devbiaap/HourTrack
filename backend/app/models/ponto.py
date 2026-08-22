from datetime import datetime, date, time
from sqlalchemy import Column, Integer, Date, Time, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Ponto(Base):
    __tablename__ = "pontos"

    id = Column(Integer,
                primary_key=True,
                index = True)

    usuario_id = Column(Integer,
                        ForeignKey("usuarios.id"),
                        nullable=False)

    data = Column(Date,
                  nullable=False)

    entrada = Column(Time,
                     nullable=False)
    saida_almoco = Column(Time,
                          nullable=True)
    volta_almoco = Column(Time,
                          nullable=True)
    saida = Column(Time,
                   nullable=True)

    observacao = Column(String(500),
                        nullable=True)

    saldo_minutos = Column(Integer,
                           nullable=False,
                           default=0)

    usuario = relationship("Usuario",
                           backref="pontos")