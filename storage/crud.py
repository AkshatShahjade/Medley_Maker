# crud.py

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from .initialize_sql import get_engine
from .sql_schema import Song, Piece, Medley

# =====================================================
# Generic CRUD
# =====================================================

def save(obj):
    """
    Insert or update an ORM object.
    """
    with Session(get_engine()) as session:
        obj = session.merge(obj)
        session.commit()
        session.refresh(obj)
        return obj


def delete(obj):
    """
    Delete an ORM object.
    """
    with Session(get_engine()) as session:
        obj = session.merge(obj)
        session.delete(obj)
        session.commit()


def get_by_id(model, id_):
    with Session(get_engine()) as session:
        return session.get(model, id_)


def get_all(model):
    with Session(get_engine()) as session:
        return list(session.scalars(select(model)))


# =====================================================
# Song Queries
# =====================================================

def search_songs(
    name: str | None = None,
    url: str | None = None,
    release_year: int | None = None,
) -> list[Song]:

    with Session(get_engine()) as session:

        query = select(Song).options(joinedload(Song.pieces))

        if name:
            query = query.where(Song.name.contains(name))

        if url:
            query = query.where(Song.url.contains(url))

        if release_year is not None:
            query = query.where(Song.release_year == release_year)

        return list(session.scalars(query).unique())


# =====================================================
# Piece Queries
# =====================================================

def search_pieces(
    name: str | None = None,
    emotion: float | None = None,
    energy: float | None = None,
    tempo: float | None = None,
    song_id: int | None = None,
    medley_name: str | None = None,
) -> list[Piece]:

    with Session(get_engine()) as session:

        query = select(Piece).options(joinedload(Piece.song)).options(joinedload(Piece.medleys))

        if name:
            query = query.where(Piece.name.contains(name))

        if emotion is not None:
            query = query.where(Piece.emotion == emotion)

        if energy is not None:
            query = query.where(Piece.energy == energy)

        if tempo is not None:
            query = query.where(Piece.tempo == tempo)

        if song_id is not None:
            query = query.where(Piece.song_id == song_id)

        if medley_name:
            query = query.where(Piece.medleys.any(Medley.name == medley_name))

        return list(session.scalars(query).unique())


# =====================================================
# Medley Queries
# =====================================================

def search_medleys(
    name: str | None = None,
    nickname: str | None = None,
) -> list[Medley]:

    with Session(get_engine()) as session:

        query = select(Medley).options(joinedload(Medley.pieces))

        if name:
            query = query.where(Medley.name.contains(name))

        if nickname:
            query = query.where(Medley.nickname.contains(nickname))

        return list(session.scalars(query).unique())