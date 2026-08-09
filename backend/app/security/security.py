import os
from dotenv import load_dotenv 
from pwdlib import PasswordHash
from jose import jwt 
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.usuario import Usuario

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

def criar_hash_senha(senha:str):
    return password_hash.hash(senha)

def verificar_senha(senha:str,
                    senha_hash:str):
    return password_hash.verify(senha,senha_hash)

def criar_token(dados: dict):
    return jwt.encode(dados,SECRET_KEY,algorithm=ALGORITHM)

oauth2_scheme = HTTPBearer()

def get_usuario_atual(credenciais: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
                      db: Session = Depends(get_db)):
    token = credenciais.credentials
    
    try:
        payload = jwt.decode(token,
                             SECRET_KEY,
                             algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(status_code = 401,
                                detail = "Token inválido")

    except Exception:
        raise HTTPException(status_code = 401,
                            detail = "Token inválido ou expirado")

    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if usuario is None:
        raise HTTPException(status_code = 401,
                            detail = "Usuário não encontrado")
    return usuario