from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UserCreate, UserUpdate
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

@router.get("/me")
def meu_usuario(usuario_atual: Usuario = Depends(get_usuario_atual)):
    return {"id": usuario_atual.id,
            "nome": usuario_atual.nome,
            "email": usuario_atual.email,
            "cargo": usuario_atual.cargo,
            "data_criacao": usuario_atual.data_criacao}

@router.get("/")
def listar_usuarios(db:Session = Depends(get_db),
                    usuario_atual: Usuario = Depends(get_usuario_atual)):
    if usuario_atual.cargo != "RH":
        raise HTTPException(status_code=403,
                            detail="Apenas o RH pode visualizar todos os usuarios")
    
    usuarios = db.query(Usuario).all()

    return usuarios

@router.put("/{usuario_id}")
def editar_usuario(usuario_id: int,
                   dados : UserUpdate,
                   db: Session = Depends(get_db),
                   usuario_atual: Usuario =  Depends(get_usuario_atual)):

    if usuario_atual.cargo != "RH":
        raise HTTPException(status_code=403,
                            detail= "Apenas o RH pode editar usuários")

    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if usuario is None:
        raise HTTPException(status_code=404,
                            detail="Usuário não encontrado")

    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.email is not None:
            usuario.email = dados.email

    if dados.nome is not None:
            usuario.nome = dados.nome

    db.commit()
    db.refresh(usuario)

    return {"mensagem": "Usuário atualizado com sucesso!",
            "usuario": {"id": usuario.id,
                        "nome": usuario.nome,
                        "email": usuario.email,
                        "cargo": usuario.cargo,
                        "data_criacao": usuario.data_criacao}}
