from sqlmodel import Session, select
from app.models.style import Style
from app.schemas.style import StyleCreate

def create_style(session: Session, style_in: StyleCreate) -> Style:
    db_style = Style.model_validate(style_in)
    session.add(db_style)
    session.commit()
    session.refresh(db_style)
    return db_style

def get_styles(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Style).offset(skip).limit(limit)).all()
