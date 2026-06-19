from sqlalchemy import (
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import Table, Column
import datetime

CURRENT_YEAR = datetime.datetime.now().year
MAX_SONG_IMPRESSION_AGE = 16

class Base(DeclarativeBase):
    pass

class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(1024))
    url: Mapped[str] = mapped_column(String(2000))
    release_year: Mapped[int]

    pieces: Mapped[list["Piece"]] = relationship(
        back_populates="song"
    )

    def getDemographic(self):
        return CURRENT_YEAR - self.release_year + MAX_SONG_IMPRESSION_AGE

medley_piece = Table(
    "medley_piece",
    Base.metadata,
    Column("medley_id", ForeignKey("medleys.id"), primary_key=True),
    Column("piece_id", ForeignKey("pieces.id"), primary_key=True),
)

class Medley(Base):
    __tablename__ = "medleys"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    nickname: Mapped[str]

    pieces: Mapped[list["Piece"]] = relationship(
        secondary=medley_piece,
        back_populates="medleys"
    )


class Piece(Base):
    __tablename__ = "pieces"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    emotion: Mapped[float]
    energy: Mapped[float]
    tempo: Mapped[float]

    st_time: Mapped[float]
    end_time: Mapped[float]

    song_id: Mapped[int] = mapped_column(
        ForeignKey("songs.id")
    )

    song: Mapped["Song"] = relationship(
        back_populates="pieces"
    )

    medleys: Mapped[list["Medley"]] = relationship(
        secondary=medley_piece,
        back_populates="pieces"
    )
