from pwdlib import PasswordHash
from jose import jwt 

SECRET_KEY = "hourtrack-chave-secreta"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

def criar_hash_senha(senha:str):
    return password_hash.hash(senha)

def verificar_senha(senha:str,
                    senha_hash:str):
    return password_hash.verify(senha,senha_hash)

def criar_token(dados: dict):
    return jwt.encode(dados,SECRET_KEY,algorithm=ALGORITHM)
