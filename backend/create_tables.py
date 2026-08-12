from app.database.database import Base, engine
from app.models.usuario import Usuario
from app.models.ponto import Ponto

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")