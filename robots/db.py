from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

e = create_engine('postgresql://postgres:postgres@localhost:5432/robots')

Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'
    date = Column(DateTime, primary_key=True)
    user = Column(String)
    color = Column(String)
    pre_moved = Column(Boolean)
    symbol = Column(String)
    other_colors_pre_moved = Column(Boolean, default=False)
    other_colors_moved = Column(Boolean, default=False)


Base.metadata.create_all(e)
SESSION = sessionmaker(bind=e)
