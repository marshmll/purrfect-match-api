from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()

@app.get("/")
def root():
    return {"hello", "world"}

@app.get("/user", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db, id)

@app.post("/user", response_model=schemas.User)
def create_user(user : schemas.UserCreate, db: Session = Depends(get_db)):
    db_aluno = crud.get_user_by_username(db, user.username)

    if db_aluno:
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")
    
    return crud.create_user(db, user)
