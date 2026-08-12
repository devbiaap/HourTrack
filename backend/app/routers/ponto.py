from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.ponto import Ponto
from app.models.usuario import Usuario
from app.schemas.ponto import PontoCreate
from app.security.security import get_usuario_atual
from app.services.calculo_horas import calcular_horas_trabalhadas


router =  APIRouter(prefix="/pontos",
                    tags=["Pontos"])

@router.post("/")
def registrar_ponto(dados: PontoCreate,
                    db: Session=Depends(get_db),
                    usuario_atual: Usuario = Depends(get_usuario_atual)):
    resultado = calcular_horas_trabalhadas(entrada=dados.entrada,
                                           saida_almoco=dados.saida_almoco,
                                           volta_almoco=dados.volta_almoco,
                                           saida=dados.saida)
    
    novo_ponto = Ponto(usuario_id=usuario_atual.id,
                       data=dados.data,
                       entrada=dados.entrada,
                       saida_almoco=dados.saida_almoco,
                       volta_almoco=dados.volta_almoco,
                       saida=dados.saida,
                       observacao=dados.observacao)

    db.add(novo_ponto)
    db.commit()
    db.refresh(novo_ponto)

    return{"message": "Ponto registrado com sucesso!",
           "ponto": {"id": novo_ponto.id,
                     "usuario": novo_ponto.usuario_id,
                     "data": novo_ponto.data,
                     "entrada": novo_ponto.entrada,
                     "saida_almoco": novo_ponto.saida_almoco,
                     "volta_almoco": novo_ponto.volta_almoco,
                     "saida": novo_ponto.saida,
                     "observacao": novo_ponto.observacao},
                     "calculo": resultado},
    


@router.get("/meus-pontos")
def meus_pontos(db: Session = Depends(get_db),
                usuario_atual: Usuario = Depends(get_usuario_atual)):
    pontos = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id).order_by(Ponto.data.desc()).all())

    return pontos