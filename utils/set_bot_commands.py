from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("help", "info"),
            types.BotCommand("keywords", "search articles"),
            types.BotCommand("accession", "search sequences"),
            # types.BotCommand("phylogeny", "build phylogenetic tree"),
        ]
    )
