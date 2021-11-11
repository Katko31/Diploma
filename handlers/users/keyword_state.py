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


@dp.callback_query_handler(text_contains="first")
async def show_first_seven_articles(call: CallbackQuery):
    await call.answer(cache_time=60)
    logging.info(f"{call.data=}")
    keywords = list(call.data.split(":"))[1]
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
