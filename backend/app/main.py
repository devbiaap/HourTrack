from fastapi import FastAPI
from app.routers import usuario, auth

app = FastAPI()

app.include_router(usuario.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return{"message": "Bem vindo(a) à API do HourTrack!"}

