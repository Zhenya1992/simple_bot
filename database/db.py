from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL='sqlite:///simple_bot.db'

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

