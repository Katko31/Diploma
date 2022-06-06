from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "запуск"),
            types.BotCommand("help", "справка"),
            types.BotCommand("keywords", "искать статьи"),
            types.BotCommand("accession", "искать последовательность"),
            types.BotCommand("phylogeny", "строить филоген дерево"),
        ]
    )
