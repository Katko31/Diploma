from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список доступных команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/keywords - Получить 7 статей по ключевым словам")

    await message.answer("\n".join(text))
