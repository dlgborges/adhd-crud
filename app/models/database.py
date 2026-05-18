import os
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# No Render, configure a variável de ambiente DATABASE_URL
print("DATABASE_URL", os.getenv("DATABASE_URL"))
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@ep-shiny-pond.neon.tech/neondb")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Objetivo(Base):
    __tablename__ = "objetivos"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descricao = Column(String)
    prazo_dias = Column(Integer)
    data_inicio = Column(Date)
    data_fim = Column(Date) 

def init_db():
    Base.metadata.create_all(bind=engine)
