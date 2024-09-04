from typing import Optional
from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name = user.name,
        username = user.username,
        date_birth = user.date_birth,
        datetime_register = user.datetime_register,
        pass_hash = user.pass_hash,
        role = user.role,
        contact_email = user.contact_email,
        contact_phone = user.contact_phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user