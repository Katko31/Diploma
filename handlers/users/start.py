from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Приветствую, {message.from_user.full_name}!\n"
                         f"Для знакомства с моими возможностями введи команду /help")
