from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.dispatcher.storage import FSMContext
from utils.misc.pubmed_parser import *
from keyboards.inline.pubmed_keywords import *


@dp.message_handler(state='enter_keywords')
async def show_pubmed_items(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(text=f"{name}", reply_markup=keywords_buttons(name))

    await state.reset_state()


@dp.message_handler(Command("keywords"))
async def find_keywords_article(message: Message, state: FSMContext):
    await message.answer('Введите ключевое слово или слова через пробел для поиска статей')
    await state.set_state('enter_keywords')


# @dp.callback_query_handler(text_contains="default")
@dp.callback_query_handler(first_seven_articles_callback.filter())
async def show_first_seven_articles(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"{call.data=}")
    # keywords = list(call.data.split(":"))[1]
    keywords = callback_data.get("keywords")
    logging.info(f"{keywords}")
    article_id = get_article_id(keywords)
    logging.info(f"{article_id=}")

    for i in article_id:
        info, url = get_article_info(i)
        # url = None
        logging.info(f"{info=}")
        logging.info(f"{url=}")
        await bot.send_message(chat_id=call.from_user.id,
                               text=info,
                               parse_mode=ParseMode.MARKDOWN, #еще одно гавно которое работает от раза к разу.
                               # Что-то парсится через маркдаун, а что-то только через хтмл, надо что-то делать
                               reply_markup=url_and_gost_buttons(i, url))


@dp.message_handler(state='enter_journal')
async def articls_and_journal(message: types.Message, state: FSMContext):
    journal_name = message.text
    async with state.proxy() as data:
        keywords = data['key']
    await message.answer(text=f"Ключевые слова для поиска: {keywords} в журнале: {journal_name}")

    await state.reset_state()


@dp.callback_query_handler(journal_callback.filter())
async def set_journal_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        data['key'] = callback_data.get("keywords")
    # keywords = callback_data.get("keywords")
    logging.info(f"{data['key']}")
    await bot.send_message(chat_id=call.from_user.id, text="Введите название журнала", reply_markup=None)
    await state.set_state('enter_journal')
