import jwt
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, time
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import security
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()   

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise security.CREDENTIALS_EXPIRATION_HTTPEXCEPTION
        
        token_data = security.TokenData(username=username)
    except InvalidTokenError:
        raise security.CREDENTIALS_EXPIRATION_HTTPEXCEPTION
    
    user = crud.get_user_by_username(db, token_data.username)

    if user is None:
        raise security.CREDENTIALS_EXPIRATION_HTTPEXCEPTION
    
    return user

@app.post("/auth")
def get_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise security.UNAUTHORIZED_HTTPEXCEPTION
    
    access_token_expires = timedelta(hours=security.AUTH_TOKEN_LIFETIME_IN_HOURS)
    access_token = crud.create_auth_token(
        data={"sub": user.username}, expiration_delta=access_token_expires
    )
    return security.Token(access_token=access_token, token_type="bearer")

# USER ============================================================================================

@app.get("/user", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    res = crud.get_user_by_id(db, id)

    if not res:
        raise HTTPException(status_code=404, detail="Usuário não encontrado no banco de dados.")
    return res

@app.get("/user/me/", response_model=schemas.User)
def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

@app.post("/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")
    
    return crud.create_user(db, user)

# CAT =============================================================================================

@app.get("/cat", response_model=schemas.Cat)
def get_cat(id: int, db: Session = Depends(get_db)):
    res = crud.get_cat_by_id(db, id)
    if not res:
        raise HTTPException(status_code=404, detail="Gato não encontrado no banco de dados.")

    return res

@app.post("/cat", response_model=schemas.Cat)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    db_cat = crud.get_cat_by_name(db, cat.name)

    if db_cat:
        raise HTTPException(status_code=400, detail="Gato de mesmo nome já cadastrado.")

    return crud.create_cat(db, cat)
