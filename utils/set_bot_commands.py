from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("keywords", "Поиск статей по ключевым словам"),
            types.BotCommand("author", "Поиск статей по автору"),
            types.BotCommand("accession", "Поиск в NCBI последовательностей по accession number"),
        ]
    )
