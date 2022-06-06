from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from data.config import PATH_TO_FASTA_ALN
from pathlib import Path
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio import AlignIO
from Bio.Align.Applications import MafftCommandline
import matplotlib
import matplotlib.pyplot as plt
import sys
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

            with open(f"{PATH_TO_FASTA_ALN}/{file_name}", "w") as handle:
                handle.write(stdout)

            align = AlignIO.read(f"{PATH_TO_FASTA_ALN}/{file_name}", "fasta")
            calculator = DistanceCalculator('identity')
            constructor = DistanceTreeConstructor(calculator)
            tree = constructor.build_tree(align)
            # Phylo.write(tree, "tree.xml", "phyloxml")

            # fig = Phylo.draw(tree)

            fig = plt.figure(figsize=(13, 5), dpi=100)
            matplotlib.rc('font', size=12)
            matplotlib.rc('xtick', labelsize=10)
            matplotlib.rc('ytick', labelsize=10)
            axes = fig.add_subplot(1, 1, 1)
            Phylo.draw(tree, axes=axes)
            fig.savefig(f"{PATH_TO_FASTA_ALN}/temporar_name")


            # await message.answer(text=f"документ сохранился по адресу: {path_to_download}")
            await message.answer_photo(types.InputFile(f"{PATH_TO_FASTA_ALN}/temporar_name.png"))

        except Exception as e:
            await message.answer(text=f"{e}")

        finally:
            await state.reset_state()

    else:
        await message.answer(text="Отправлять можно только документы")

    filelist = glob.glob(os.path.join(PATH_TO_FASTA_ALN, "*"))
    for f in filelist:
        os.remove(f) #TODO модифицировать!
    await state.reset_state()


@dp.message_handler(Command("phylogeny"))
async def send_fasta(message: Message, state: FSMContext):
    await message.answer('Отправь мне один multi FASTA файл с несколькими последовательностями')
    await state.set_state('enter_fasta')
