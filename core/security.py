from hashlib import sha256
from secrets import token_hex
from pydantic import BaseModel

ALGORITHM = "HS256"
SECRET_KEY = "nope"
AUTH_TOKEN_LIFETIME_IN_MINUTES = 30

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