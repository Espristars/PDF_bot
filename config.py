from dotenv import load_dotenv
from aiogram import Bot
import os

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

config = Config()

bot = Bot(token=config.BOT_TOKEN)