import asyncio
import logging
import datetime

from aiogram import Router, types, F, Bot
from aiogram.filters import or_f
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

from bot.filters.chat_tipes import ChatTypeFilter
from bot.handlers.parse_to_exexl import create_excel_from_dict_list
from bot.handlers.parsing2 import parsing

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

flag = True
logging.basicConfig(level=logging.INFO)


async def send_document(message: types.Message, bot):
    document = FSInputFile("./excel_files/companies.xlsx")
    await bot.send_document(message.chat.id, document)
    logging.info("Документ отправлен")


@user_private_router.message(or_f(Command('start'), F.text.lower().contains('старт')))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я ваш бот парсер.")

@user_private_router.message(or_f(Command('document'), F.text.lower().contains('получить документ')))
async def send_exel(message: types.Message, bot: Bot):
    await message.answer("Вот эксель документ")
    await send_document(message, bot)
last = [0, 0]
@user_private_router.message(or_f(Command('parse'), F.text.lower().contains('парсинг')))
async def cmd_parse(message: types.Message, bot: Bot):
    await message.answer("Парсер работает")
    global flag
    if flag:
        flag = False
        logging.info("парсер запущен")
        while True:
            last.append(parsing())
            del last[0]
            if 0 not in last and last[0] != last[1]:
                for i in range(len(last[0])):
                    if list(last[0][i].values()) != list(last[1][i].values()):
                        await message.answer(f"{i + 1}")
                        for k in last[i][0]:
                            if last[0][i][k] != last[1][i][k]:
                                await message.answer(last[1][i][k])
            create_excel_from_dict_list(last[-1], 'companies.xlsx')
            if int(str(datetime.datetime.now().time()).split(".")[0].split(":")[0]) == 0:
                await send_document(message, bot)
            await asyncio.sleep(600)