from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UserLogin
from app.database.database import get_db
from app.models.usuario import Usuario
from app.security.security import verificar_senha, criar_token

router = APIRouter(prefix="/auth",
                   tags=["Autenticação"])

@router.post("/login")
def login(dados: UserLogin, db:Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario:
        raise HTTPException(status_code=401,
                            detail="E-mail ou senha incorretos")

    if not verificar_senha(dados.senha,
                           usuario.senha):
        raise HTTPException(status_code=401,
                            detail="E-mail ou senha incorretos")

    token = criar_token({"sub":str(usuario.id),
                        "cargo": usuario.cargo})

    return {"message": "Login realizado com sucesso!",
            "access_token": token,
            "token_tipe": "bearer"}