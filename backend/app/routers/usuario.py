from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UserCreate
from app.database.database import get_db
from app.models.usuario import Usuario
from app.security.security import criar_hash_senha, get_usuario_atual

router = APIRouter(prefix="/usuarios",
                   tags=["Usuários"])

@router.post("/")
def criar_usuario(usuario: UserCreate, db: Session = Depends(get_db),
                  usuario_atual: Usuario = Depends(get_usuario_atual)):
    if usuario_atual.cargo != "RH":
        raise HTTPException(status_code=403,
                            detail="Apenas o RH pode cadastrar usuários")
    
    senha_hash = criar_hash_senha(usuario.senha)

    novo_usuario = Usuario(nome=usuario.nome,
                           email=usuario.email,
                           senha=senha_hash,
                           cargo=usuario.cargo,
                           data_criacao=usuario.data_criacao)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return{"mensagem": "Usuário cadastrado com sucesso!",
           "usuario": {"id": novo_usuario.id,
                       "nome": novo_usuario.nome,
                       "email": novo_usuario.email,
                       "cargo": novo_usuario.cargo,
                       "data_criacao": novo_usuario.data_criacao}}
    