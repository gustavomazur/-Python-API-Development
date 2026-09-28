import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(
        "Variavel SQLALCHEMY_DATABASE_URL nao encontrada.\n"
        "Crie o arquivo .env na raiz do projeto a partir do .env.example:\n"
        "    cp .env.example .env"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Ela vai criar uma sessão com nosso banco de dados para cada requisição feita a esse endpoint específico da API.
#Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()