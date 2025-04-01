import logging
import time

import schedule
from aiogram import Router, types, F, Bot
from aiogram.filters import or_f
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputFile
from aiogram.utils.formatting import as_marked_section, Bold, as_list

from bot.filters.chat_tipes import ChatTypeFilter
from parse_to_exexl import create_excel_from_dict_list
from parsing2 import parsing

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

flag = True
logging.basicConfig(level=logging.INFO)


async def send_document(message: types.Message, bot):
    document = FSInputFile("./handlers/excel_files/companies.xlsx")
    await bot.send_document(message.chat.id, document)
    logging.info("Документ отправлен")


@user_private_router.message(or_f(Command('start'), F.text.lower().contains('старт')))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я ваш бот парсер.")

@user_private_router.message(or_f(Command('document'), F.text.lower().contains('получить документ')))
async def send_exel(message: types.Message, bot: Bot):
    await message.answer("Вот эксель документ")
    await send_document(message, bot)


@user_private_router.message(or_f(Command('parse'), F.text.lower().contains('парсинг')))
async def cmd_parse(message: types.Message, bot: Bot):
    await message.answer("Парсер работает")
    global flag
    if flag:
        flag = False
        schedule.every(10).minutes.do(create_excel_from_dict_list(parsing(), 'companies.xlsx'))
        schedule.every().day.at("14:21").do(send_document(message, bot))
        logging.info("парсер запущен")
