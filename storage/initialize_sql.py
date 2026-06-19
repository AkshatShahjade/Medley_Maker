from sqlalchemy import create_engine
from .sql_schema import Base, Song

engine = None

def initialize_db():
    global engine
    engine = create_engine("sqlite:///medleys.db")
    Base.metadata.create_all(engine)

def get_engine():
    global engine
    if(engine is None):
        engine = create_engine("sqlite:///medleys.db")
    return engine

