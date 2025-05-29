from aiogram.types import Message


async def handle_start(msg: Message):
    await msg.answer("Привет, отправь мне файл *.pdf и я верну тебе таблицу из этого файла!")