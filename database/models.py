from sqlalchemy.orm import relationship

from database.db import Base
from sqlalchemy import Integer, Column, String, DateTime, func, ForeignKey

class Users(Base):
    """Класс пользователей"""


    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    registrate_at = Column(DateTime, default=func.now())

    messages = relationship('MessageLog', back_populates='user', )


class MessageLog(Base):
    """Класс логов"""

    __tablename__ = 'messagelog'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message_text = Column(String)
    timestamp = Column(DateTime, default=func.now())

    user = relationship('Users', back_populates='messages')

