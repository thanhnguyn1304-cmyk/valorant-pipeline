from backend.core.config import settings
from sqlmodel import Session, create_engine

engine = create_engine(settings.CONNECTION_STRING, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
