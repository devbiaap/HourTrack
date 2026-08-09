from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.usuario import UserCreate
from app.database.database import get_db
from app.models.usuario import Usuario
from app.security.security import criar_hash_senha

router = APIRouter(prefix="/usuarios",
                   tags=["Usuários"])

@router.post("/")
def criar_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    
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
    