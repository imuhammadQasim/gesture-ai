from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(session: Session, user_in: UserCreate) -> User:
    db_user = User.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(User).offset(skip).limit(limit)).all()
