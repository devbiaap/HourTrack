from fastapi import FastAPI

app = FastAPI(title="HourTrack API",
              version="1.0.0")

@app.get("/")
def home():
    return{"messpiage": "Bem vindo(a) à API do HourTrack!"}

