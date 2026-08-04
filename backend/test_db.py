from sqlalchemy import text
from app.database.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())
    