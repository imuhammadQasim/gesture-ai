from sqlmodel import Session, select
from app.models.generation import Generation
from app.schemas.generation import GenerationCreate

def create_generation(session: Session, generation_in: GenerationCreate) -> Generation:
    db_generation = Generation.model_validate(generation_in)
    # Placeholder: Usually we would trigger AI processing here
    # and update the status later via a worker.
    session.add(db_generation)
    session.commit()
    session.refresh(db_generation)
    return db_generation

def get_generations(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Generation).offset(skip).limit(limit)).all()
