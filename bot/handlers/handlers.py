import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os


from bot.handlers.commands import handle_start
from bot.service_functions import file_convert_pdf_to_json, file_convert_photo_to_text
from config import bot

router = Router()

router.message.register(handle_start, Command("start"))


async def handle_photo(msg: Message):

    file = await msg.bot.get_file(msg.document.file_id)
    file_path = file.file_path

    os.makedirs("photos", exist_ok=True)
    local_filename = os.path.join("photos", msg.document.file_name)
    await bot.download_file(file_path, local_filename)

    path_json = await file_convert_photo_to_text(local_filename)

    os.remove(local_filename)

    document = FSInputFile(path_json)

    await msg.answer_document(document)

    os.remove(path_json)


@router.message(F.content_type == 'document')
async def handle_file(msg: Message):

    if msg.document.file_name.lower().endswith(".jpeg"):
        asyncio.create_task(handle_photo(msg))
        return
    if not msg.document.file_name.lower().endswith(".pdf"):
        await msg.reply("Пожалуйста, отправьте файл в формате *.pdf!")
        return

    file = await msg.bot.get_file(msg.document.file_id)
    file_path = file.file_path

    os.makedirs("documents", exist_ok=True)
    local_filename = os.path.join("documents", msg.document.file_name)
    await bot.download_file(file_path, local_filename)

    path_json = await file_convert_pdf_to_json(local_filename)

    os.remove(local_filename)

    document = FSInputFile(path_json)

    await msg.answer_document(document)

    os.remove(path_json)


@router.message(F.text)
async def handle_text(msg: Message):
    await msg.answer("Отправь мне файл *.pdf!")
