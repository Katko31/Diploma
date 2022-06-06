from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список доступных команд: ", '\n'
            "/start - начать диалог", '\n'
            "/help - получить справку", '\n'
            "/keywords - искать статьи по ключевым словам, можно с дополнительными фильтрами (автор, журнал)", '\n'
            "/accession - получить FASTA файл последовательности по accession number из базы данных NCBI “protein” или "
            "“nucleotide”", '\n'
            "/phylogeny - построить филогенетическое дерево на основании fasta файла с последовательностями "
            "(последовательностей в файле должно быть минимум 2) и, в качестве вывода, получить изображение "
            "филогенетической реконструкции")

    await message.answer("\n".join(text))
