from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# In production for PostgreSQL, we would change the connection URL format.
# `check_same_thread=False` is needed only for SQLite.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG, # Print SQL queries when in DEBUG mode
    connect_args=connect_args
)

def create_db_and_tables():
    # Will create tables based on imported SQLModel classes
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
