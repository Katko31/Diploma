from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from data.config import PATH_TO_FASTA_ALN
from pathlib import Path
from Bio.Align.Applications import MafftCommandline
import os, glob


@dp.message_handler(state='enter_fasta', content_types=types.ContentTypes.ANY)
async def create_phylogenetic(message: types.Message, state: FSMContext):
    logging.info(f"{type(message)=}")
    if message.document:
        try:
            file_name = message.document.file_name #TODO проверить, что формат fasta в названии нет неправильных символов

            logging.info(f"{file_name=}")
            path_to_download = Path().joinpath(PATH_TO_FASTA_ALN)
            path_to_download = path_to_download.joinpath(message.document.file_name)
            await message.document.download(destination=path_to_download)

            cline = MafftCommandline("mafft", input=path_to_download)
            stdout, stderr = cline()

            with open(f"{PATH_TO_FASTA_ALN}/{file_name}.aln", "w") as handle:
                handle.write(stdout)

            await message.answer(text=f"документ сохранился по адресу: {path_to_download}")

        except Exception as e:
            await message.answer(text=f"{e}")

        finally:
            await state.reset_state()

    else:
        await message.answer(text="Отправлять можно только документы")

    # filelist = glob.glob(os.path.join(PATH_TO_FASTA_ALN, "*"))
    # for f in filelist:
    #     os.remove(f) #TODO модифицировать а то удалятся все документы, которые там сохранятся от других пользователей
    await state.reset_state()


@dp.message_handler(Command("phylogeny"))
async def send_fasta(message: Message, state: FSMContext):
    await message.answer('Отправьте мне fasta файл с последовательностями')
    await state.set_state('enter_fasta')
