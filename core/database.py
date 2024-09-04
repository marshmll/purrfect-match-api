from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

USERNAME = "renan"
PASSWORD = "andrade16"
HOST = "localhost"
PORT = "3306"
DATABASE = "purrfect_db"

DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(
    url=DATABASE_URL,
    # connect_args={"check_same_thread": False}, # ONLY FOR SQLITE
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()