import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from . import models, schemas, security

# AUTHENTICATION

def create_auth_token(data: dict, expiration_delta: timedelta):
    to_encode = data.copy()
    
    if expiration_delta:
        expiration = datetime.now(timezone.utc) + expiration_delta
    else:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, security.SECRET_KEY, security.ALGORITHM)

    return encoded_jwt

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)

    if user is None:
        return False
    elif not security.check_password(user.pass_salt, user.pass_hash, password):
        return False
    
    return user

# USER ============================================================================================

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    salt = security.gen_salt()
    db_user = models.User(
        name = user.name,
        username = user.username,
        date_birth = user.date_birth,
        datetime_register = user.datetime_register,
        pass_salt = salt,
        pass_hash = security.hash_password(salt, user.password),
        role = user.role,
        contact_email = user.contact_email,
        contact_phone = user.contact_phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# CAT =============================================================================================

def get_cat_by_id(db: Session, id: int):
    return db.query(models.Cat).filter(models.Cat.id == id).first()

def get_cat_by_name(db: Session, name: str):
    return db.query(models.Cat).filter(models.Cat.name == name).first()

def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat (
        name = cat.name,
        age = cat.age,
        sex = cat.sex,
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)

    return db_cat
