from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список доступных команд: ",
            "/start - начать диалог",
            "/help - получить справку",
            "/keywords - искать статьи по ключевым словам, и, при необходимости, с дополнительными фильтрами (автор, журнал)",
            "/accesiion - получить последовательность(-и) в формате fasta из базы данных nucleotide или protein",
            "/phylogeny - построить филогенетическое дерево на основании вашего fasta файла с последовательностями")

    await message.answer("\n".join(text))
