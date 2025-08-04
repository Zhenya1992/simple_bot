from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command


from database.db import SessionLocal
from database.models import Users
router = Router()

@router.message(CommandStart())
async def command_start_handler(message:types.Message):
    """Обработчик реакции на команду старт и ссылку"""

    session = SessionLocal()

    tg_id = message.from_user.id

    user = session.query(Users).filter(Users.telegram_id==tg_id).first()

    if not user:
        user = Users(
            telegram_id=tg_id,
            username=message.from_user.username
        )

        session.add(user)
        session.commit()
        await message.answer("Вы зареганы!!!!!")

    session.close()

@router.message(Command('help'))
async def help_handler(message:types.Message):
    """..."""

    session = SessionLocal()

    user = session.query(Users).filter(Users.telegram_id==message.from_user.id).first()

    if user:
        await message.answer(
            f"Ваш id: {user.telegram_id}\n"
            f"Ваш ник: {user.username}\n"
            f"Дата регистрации: {user.registrate_at}"
        )
    else:
        await message.answer("Вы не зареганы!!!!!")

    session.close()