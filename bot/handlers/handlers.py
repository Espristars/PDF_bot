import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile
import logging
import os


from bot.handlers.commands import handle_start
from bot.service_functions import file_convert_pdf_to_json, file_convert_photo_to_text
from config import bot

router = Router()

logger = logging.getLogger()

router.message.register(handle_start, Command("start"))


async def handle_photo_file(msg: Message):

    try:
        index_col, index_str = msg.caption.split(" ")
        index_col = int(index_col)
        index_str = int(index_str)
    except Exception as e:
        logger.info(f"{e}")
        await msg.answer("Направьте 2 числа: количество столбцов и количество строк")
        return
    file = await msg.bot.get_file(msg.document.file_id)
    file_path = file.file_path

    os.makedirs("photos", exist_ok=True)
    local_filename = os.path.join("photos", msg.document.file_name)
    await bot.download_file(file_path, local_filename)

    try:
        path_json = await file_convert_photo_to_text(local_filename, index_col, index_str)
    except Exception as e:
        await msg.answer(f"{e}")
        return
    os.remove(local_filename)

    document = FSInputFile(path_json)

    await msg.answer_document(document)

    os.remove(path_json)


@router.message(F.photo)
async def handle_photo(msg: Message):

    try:
        index_col, index_str = msg.caption.split(" ")
        index_col = int(index_col)
        index_str = int(index_str)
    except Exception as e:
        logger.info(f"{e}")
        await msg.answer("Направьте 2 числа: количество столбцов и количество строк")
        return
    file = await msg.bot.get_file(msg.photo[-1].file_id)
    file_path = file.file_path

    os.makedirs("photos", exist_ok=True)
    file_name = f"{msg.from_user.id}_{msg.message_id}.jpg"
    local_filename = os.path.join("photos", file_name)
    await bot.download_file(file_path, local_filename)

    try:
        path_json = await file_convert_photo_to_text(local_filename, index_col, index_str)
    except Exception as e:
        await msg.answer(f"{e}")
        return
    os.remove(local_filename)

    document = FSInputFile(path_json)

    await msg.answer_document(document)

    os.remove(path_json)


@router.message(F.content_type == 'document')
async def handle_file(msg: Message):

    if msg.document.file_name.lower().endswith(".jpeg" or ".png" or ".jpg"):
        asyncio.create_task(handle_photo_file(msg))
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
