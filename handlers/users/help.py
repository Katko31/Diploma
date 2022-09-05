from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("List of comands: ", '\n'
            "/start - start dialog", '\n'
            "/help - get info", '\n'
            "/keywords - search articles by kew words (available filters: “author“ and “journal“)", '\n'
            "/accession - retrieve FASTA file by sequence accession number from NCBI “protein“ or “nucleotide“ database", '\n')
            # "/phylogeny - build phylogenetic tree with your sequences."
            # "As input add one FASTA file with minimum 2 sequences. As output you will get a picture with phylogenetic reconstruction")

    await message.answer("\n".join(text))
