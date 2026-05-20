from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

comic_tag_table = Table(
    "comic_tags",
    Base.metadata,
    Column("comic_id", Integer, ForeignKey("comics.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    path = Column(String, nullable=False, unique=True)
    format = Column(String, nullable=False)
    rating = Column(Integer, default=0)
    page_count = Column(Integer, nullable=True)

    tags = relationship("Tag", secondary=comic_tag_table, back_populates="comics")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)

    comics = relationship("Comic", secondary=comic_tag_table, back_populates="tags")