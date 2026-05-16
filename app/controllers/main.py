from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Objetivo, Usuario
from app.controllers.auth import criar_token, verificar_senha, hash_senha

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# AUTH ROUTES
@router.post("/auth/register")
def register(dados: dict, db: Session = Depends(get_db)):
    novo_user = Usuario(username=dados['username'], password_hash=hash_senha(dados['password']))
    db.add(novo_user)
    db.commit()
    return {"status": "sucesso"}

@router.post("/auth/login")
def login(dados: dict, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == dados['username']).first()
    if not user or not verificar_senha(dados['password'], user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"token": criar_token({"sub": user.username})}

# CRUD OBJETIVOS
@router.get("/objetivos")
def listar_objetivos(db: Session = Depends(get_db)):
    return db.query(Objetivo).all()

@router.post("/objetivos")
def criar_objetivo(objetivo: dict, db: Session = Depends(get_db)):
    novo = Objetivo(titulo=objetivo['titulo'], descricao=objetivo['descricao'], )
    db.add(novo)
    db.commit()
    return {"status": "criado"}

@router.put("/objetivos/{id}")
def editar_objetivo(id: int, dados: dict, db: Session = Depends(get_db)):
    objetivo = db.query(Objetivo).filter(Objetivo.id == id).first()
    if not objetivo: raise HTTPException(status_code=404)
    objetivo.titulo = dados['titulo']
    objetivo.descricao = dados['descricao']
    db.commit()
    return {"status": "atualizado"}

@router.delete("/objetivos/{id}")
def excluir_objetivo(id: int, db: Session = Depends(get_db)):
    objetivo = db.query(Objetivo).filter(Objetivo.id == id).first()
    if not objetivo: raise HTTPException(status_code=404)
    db.delete(objetivo)
    db.commit()
    return {"status": "removido"}
