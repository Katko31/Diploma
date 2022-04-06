from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline.ncbi_accession import *
from aiogram.dispatcher.storage import FSMContext
from utils.misc.prefix_creator import get_prefix
from utils.misc.fasta_creator import fasta_creator


@dp.message_handler(state='enter_accession')
async def show_accession_items(message: types.Message, state: FSMContext):
    accession = message.text
    logging.info(f'{type(accession)}')
    await message.answer(text=f"{accession}", reply_markup=accession_buttons(accession))

    await state.reset_state()


@dp.message_handler(Command("accession"))
async def find_accession_number(message: Message, state: FSMContext):
    await message.answer('Введите accession number искомой последовательности')
    await state.set_state('enter_accession')


@dp.callback_query_handler(accession_callback.filter())
async def download_accession_number(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    accession = callback_data.get("accession")
    logging.info(f"{accession=}")

    prefix = get_prefix(accession)
    logging.info(f'{prefix=}')

    if prefix <= 2:
        logging.info(f'Условие, что префикс < 2 выполняется')
        path_to_doc = fasta_creator(accession, "nucleotide")
        logging.info(f'{path_to_doc=}')
    elif prefix == 3:
        path_to_doc = fasta_creator(accession, "protein")
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Неправильно введен accession number', reply_markup=None)

    await bot.send_document(chat_id=call.from_user.id, document=types.InputFile(path_to_doc), reply_markup=None)
    logging.info(f'Щас попрубую удалить {path_to_doc=}')
    del path_to_doc
    logging.info(f'Надеюсь, что все удалилось')
        # pass
    # else:
    #     pass
    # await message.answer_document(document=types.InputFile(path_to_doс))
    # if accession[0] or accession[0:1] or accession[0:2]
    #     """
    #     Nucleotide:
    #     1 letter + 5 numerals
    #            2 letters + 6 numerals
    #            2 letters + 8 numerals
    #
    #/home/kate/PycharmProjects/Diploma_bot/U49845.fasta
    #     Protein:
    #     3 letters + 5 numerals
    #            3 letters + 7 numerals
    #     """

