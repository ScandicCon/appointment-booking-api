from sqlmodel import create_engine, Session
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine (
        DATABASE_URL, 
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=True
    )

def get_session():
    with Session(engine) as session:
        yield session