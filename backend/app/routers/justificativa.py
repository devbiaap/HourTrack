from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.justificativa import Justificativa
from app.models.usuario import Usuario
from app.schemas.justificativa import JustificativaCreate
from app.security.security import get_usuario_atual

router = APIRouter(prefix = "/justificativas",
                   tags = ["Justificativas"])

@router.post("/")
def criar_justificativa(dados: JustificativaCreate,
                        db: Session = Depends(get_db),
                        usuario_atual: Usuario = Depends(get_usuario_atual)):
    nova_justificativa = Justificativa(usuario_id = usuario_atual.id,
                                       data = dados.data,
                                       motivo = dados.motivo)

    db.add(nova_justificativa)
    db.commit()
    db.refresh(nova_justificativa)

    return {"mensagem": "Justificativa enviada com sucesso!",
            "justificativa": {"id": nova_justificativa.id,
                              "data": nova_justificativa.data},
                              "motivo": nova_justificativa.motivo,
                              "status": nova_justificativa.status}

@router.get("/")
def listar_justificativas(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    if usuario_atual.cargo != "RH":
        raise HTTPException(
            status_code = 403,
            detail = "Apenas o RH pode visualizar as justificativas."
        )

    justificativas = (
        db.query(Justificativa)
        .order_by(Justificativa.data.desc())
        .all()
    )

    return justificativas

@router.put("/{justificativa_id}/aprovar")
def aprovar_justificativa(
    justificativa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    if usuario_atual.cargo != "RH":
        raise HTTPException(
            status_code = 403,
            detail = "Apenas o RH pode aprovar justificativas."
        )

    justificativa = (db.query(Justificativa).filter(Justificativa.id == justificativa_id).first())

    if justificativa is None:
        raise HTTPException(
            status_code = 404,
            detail = "Justificativa não encontrada."
        )

    if justificativa.status != "PENDENTE":
        raise HTTPException(
            status_code = 400,
            detail = "Essa justificativa já foi analisada."
        )

    justificativa.status = "APROVADA"

    db.commit()
    db.refresh(justificativa)

    return {
        "message": "Justificativa aprovada com sucesso!",
        "justificativa": {
            "id": justificativa.id,
            "usuario_id": justificativa.usuario_id,
            "data": justificativa.data,
            "motivo": justificativa.motivo,
            "status": justificativa.status
        }
    }

@router.put("/{justificativa_id}/recusar")
def recusar_justificativa(
    justificativa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    if usuario_atual.cargo != "RH":
        raise HTTPException(
            status_code = 403,
            detail = "Apenas o RH pode recusar justificativas."
        )

    justificativa = (
        db.query(Justificativa)
        .filter(Justificativa.id == justificativa_id)
        .first()
    )

    if justificativa is None:
        raise HTTPException(
            status_code = 404,
            detail = "Justificativa não encontrada."
        )

    if justificativa.status != "PENDENTE":
        raise HTTPException(
            status_code = 400,
            detail = "Essa justificativa já foi analisada."
        )

    justificativa.status = "RECUSADA"

    db.commit()
    db.refresh(justificativa)

    return {
        "message": "Justificativa recusada com sucesso!",
        "justificativa": {
            "id": justificativa.id,
            "usuario_id": justificativa.usuario_id,
            "data": justificativa.data,
            "motivo": justificativa.motivo,
            "status": justificativa.status
        }
    }



@router.get("/minhas")
def minhas_justificativas(db: Session = Depends(get_db),
                          usuario_atual: Usuario = Depends(get_usuario_atual)):
    justificativas = (db.query(Justificativa).filter(Justificativa.usuario_id == usuario_atual.id).order_by(Justificativa.data.desc()).all())

    return justificativas