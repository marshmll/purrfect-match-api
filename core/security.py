from os import getenv
from hashlib import sha256
from secrets import token_hex
from pydantic import BaseModel
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = getenv("JWT_KEY")
AUTH_TOKEN_LIFETIME_IN_HOURS = 48

CREDENTIALS_EXPIRATION_HTTPEXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar as credenciais",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_HTTPEXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Usuário ou senha incorretos",
    headers={"WWW-Authenticate": "Bearer"},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def gen_salt():
    return token_hex(16)

def hash_password(salt: str, password: str):
    return sha256(password.encode()).hexdigest()

def check_password(pass_salt: str, pass_hash: str, password: str):
    hashed_pass = hash_password(pass_salt, password)
    return pass_hash == hashed_pass 