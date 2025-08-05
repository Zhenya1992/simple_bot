from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
import pytz

from database.db import SessionLocal
from database.models import Users, MessageLog

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
    """Обработчик реакции на команду старт и ссылку"""

    session = SessionLocal()

    tg_id = message.from_user.id

    user = session.query(Users).filter(Users.telegram_id == tg_id).first()

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
async def help_handler(message: types.Message):
    """Обработчик реакции на команду help"""

    session = SessionLocal()

    user = session.query(Users).filter(Users.telegram_id == message.from_user.id).first()

    if user:
        await message.answer(
            f"Ваш id: {user.telegram_id}\n"
            f"Ваш ник: {user.username}\n"
            f"Дата регистрации: {user.registrate_at}"
        )
    else:
        await message.answer("Вы не зареганы!!!!!")

    session.close()


@router.message(Command('history'))
async def history_handler(message: types.Message):
    """Обработчик реакции на команду history"""

    session = SessionLocal()
    user = session.query(Users).filter(Users.telegram_id == message.from_user.id).first()

    if user:
        messages = (session.query(MessageLog)
                    .filter(MessageLog.user_id == user.id)
                    .order_by(MessageLog.timestamp.desc())
                    .limit(3)
                    .all())

        if messages:
            minsk_tz = pytz.timezone('Europe/Minsk')
            formatted_messages = []

            for m in messages:
                if m.timestamp.tzinfo is None:
                    utc_time = pytz.utc.localize(m.timestamp)
                else:
                    utc_time = m.timestamp

                minsk_time = utc_time.astimezone(minsk_tz)
                time_str = minsk_time.strftime('%d.%m.%Y %H:%M:%S')
                formatted_messages.append(f"{time_str}: {m.message_text}")

            text = "\n".join(formatted_messages)
            await message.answer(f'Последние сообщения:\n{text}')
        else:
            await message.answer('У вас пока нет сообщений в истории')
    else:
        await message.answer('Вы не зарегистрированы')

    session.close()


@router.message(F.text.regexp(r"^(?!\/).+"))
async def log_message(message: types.Message):
    """Обработчик логирования сообщений"""

    session = SessionLocal()
    user = session.query(Users).filter(Users.telegram_id == message.from_user.id).first()

    if user:
        log = MessageLog(user_id=user.id, message_text=message.text)
        session.add(log)
        session.commit()

    session.close()
