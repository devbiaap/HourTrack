from app.database.database import Base, engine
from app.models.usuarios import Usuario

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")