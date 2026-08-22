from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.ponto import Ponto
from app.models.usuario import Usuario
from app.schemas.ponto import PontoCreate
from app.security.security import get_usuario_atual
from app.services.calculo_horas import calcular_horas_trabalhadas
from datetime import date, datetime


router =  APIRouter(prefix="/pontos",
                    tags=["Pontos"])

@router.post("/")
def registrar_ponto(dados: PontoCreate,
                    db: Session=Depends(get_db),
                    usuario_atual: Usuario = Depends(get_usuario_atual)):
    ponto_existente = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id,
                                              Ponto.data == dados.data).first())
    if ponto_existente:
        raise HTTPException(status_code=400,
                            detail="Já existe um registro de ponto para este dia.")
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
                       observacao=dados.observacao,
                       saldo_minutos=resultado["diferenca_minutos"])

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
                     "observacao": novo_ponto.observacao,
                     "saldo_minutos": novo_ponto.saldo_minutos},
                     "calculo": resultado},
    


@router.get("/meus-pontos")
def meus_pontos(db: Session = Depends(get_db),
                usuario_atual: Usuario = Depends(get_usuario_atual)):
    pontos = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id).order_by(Ponto.data.desc()).all())

    return pontos

@router.get("/meu-saldo")
def meu_saldo(db: Session = Depends(get_db),
              usuario_atual: Usuario = Depends(get_usuario_atual)):
    pontos = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id).all())
    saldo_total = sum(ponto.saldo_minutos for ponto in pontos)

    horas = abs(saldo_total) // 60
    minutos = abs(saldo_total) % 60

    sinal = "+" if saldo_total > 0 else "-" if saldo_total < 0 else ""

    return{"usuario": usuario_atual.nome,
           "saldo_minutos": saldo_total,
           "saldo_horas": f"{sinal}{horas:02d}:{minutos:02d}"}

@router.post("/entrada")
def registrar_entrada(db: Session = Depends(get_db),
                      usuario_atual: Usuario = Depends(get_usuario_atual)):
    hoje = date.today()
    agora = datetime.now().time().replace(microsecond=0)

    ponto_existente = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id,
                                              Ponto.data == hoje).first())
    if ponto_existente:
        raise HTTPException(status_code=400,
                            detail= "Já existe um registro de ponto para hoje")

    novo_ponto = Ponto(usuario_id=usuario_atual.id,
                       data=hoje,
                       entrada=agora)
    db.add(novo_ponto)
    db.commit()
    db.refresh(novo_ponto)

    return {"message": "Entrada registrada com sucesso!",
            "ponto": {"id": novo_ponto.id,
                      "data": novo_ponto.data,
                      "entrada": novo_ponto.entrada}}

@router.post("/saida-almoco")
def registrar_saida_almoco(db: Session = Depends(get_db),
                      usuario_atual: Usuario = Depends(get_usuario_atual)):
    hoje = date.today()

    ponto = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id,
                                              Ponto.data == hoje).first())
    if ponto is None:
        raise HTTPException(status_code=404,
                            detail= "Nenhum ponto encontrado para hoje.")
    if ponto.entrada is None:
        raise HTTPException(status_code=400,
                                detail= "É necessário registrar a entrada primeiro.")
    if ponto.saida_almoco is not None:
        raise HTTPException(status_code=400,
                            detail="A saída para o almoço já foi registrada.")
    ponto.saida_almoco = datetime.now().time().replace(microsecond=0)

    db.commit()
    db.refresh(ponto)

    return {"message": "Saída para o almoço registrada com sucesso!",
            "ponto": {"id": ponto.id,
                      "data": ponto.data,
                      "entrada": ponto.entrada},
                      "saida-almoco": ponto.saida_almoco}

@router.post("/volta-almoco")
def registrar_volta_almoco(db: Session = Depends(get_db),
                      usuario_atual: Usuario = Depends(get_usuario_atual)):
    hoje = date.today()

    ponto = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id,
                                              Ponto.data == hoje).first())
    if ponto is None:
        raise HTTPException(status_code=404,
                            detail= "Nenhum ponto encontrado para hoje.")
    if ponto.saida_almoco is None:
        raise HTTPException(status_code=400,
                                detail= "É necessário registrar a saída para o almoço primeiro.")
    if ponto.volta_almoco is not None:
        raise HTTPException(status_code=400,
                            detail="A volta do almoço já foi registrada.")
    ponto.volta_almoco = datetime.now().time().replace(microsecond=0)

    db.commit()
    db.refresh(ponto)

    return {"message": "Saída para o almoço registrada com sucesso!",
            "ponto": {"id": ponto.id,
                      "data": ponto.data,
                      "entrada": ponto.entrada},
                      "saida-almoco": ponto.saida_almoco,
                      "volta-almoco": ponto.volta_almoco}


@router.post("/saida")
def registrar_saida(db: Session = Depends(get_db),
                      usuario_atual: Usuario = Depends(get_usuario_atual)):
    hoje = date.today()

    ponto = (db.query(Ponto).filter(Ponto.usuario_id == usuario_atual.id,
                                              Ponto.data == hoje).first())
    if ponto is None:
        raise HTTPException(status_code=404,
                            detail= "Nenhum ponto encontrado para hoje.")
    if ponto.entrada is None:
        raise HTTPException(status_code=400,
                                detail= "É necessário registrar a entrada primeiro.")
    if ponto.saida_almoco is None:
            raise HTTPException(status_code=400,
                                    detail= "É necessário registrar a saída do almoço primeiro.")
    if ponto.volta_almoco is None:
            raise HTTPException(status_code=400,
                                    detail= "É necessário registrar a volta do almoço primeiro.")
    if ponto.saida is not None:
        raise HTTPException(status_code=400,
                            detail="A saída já foi registrada.")
    ponto.saida = datetime.now().time().replace(microsecond=0)

    resultado = calcular_horas_trabalhadas(entrada=ponto.entrada,
                                           saida_almoco=ponto.saida_almoco,
                                           volta_almoco=ponto.volta_almoco,
                                           saida=ponto.saida)

    ponto.saldo_minutos = resultado["diferenca_minutos"]

    db.commit()
    db.refresh(ponto)

    return {"message": "Saída registrada com sucesso!",
            "ponto": {"id": ponto.id,
                      "data": ponto.data,
                      "entrada": ponto.entrada,
                      "saida-almoco": ponto.saida_almoco,
                      "volta-almoco": ponto.volta_almoco,
                      "saida": ponto.saida,
                      "saldo_minutos": ponto.saldo_minutos},
                      "calculo" : resultado}