from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.dispatcher.storage import FSMContext
from utils.misc.pubmed_parser import *
from keyboards.inline.pubmed_keywords import *
from data.config import ARTICLES_NUMBER
from utils.misc.url_article import create_gost_link


@dp.message_handler(state='enter_keywords')
async def show_pubmed_items(message: types.Message, state: FSMContext):
    name = message.text
    await message.answer(text=f"{name}", reply_markup=keywords_buttons(name))

    await state.reset_state()


@dp.message_handler(Command("keywords"))
async def find_keywords_article(message: Message, state: FSMContext):
    await message.answer('Введите ключевое слово или слова через пробел для поиска статей')
    await state.set_state('enter_keywords')


@dp.callback_query_handler(first_seven_articles_callback.filter())
async def show_first_seven_articles(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info(f" Что в колбэк{call.data=}")
    keywords = callback_data.get("keywords")

    journal_name = None
    exception_list = None
    author_name = None

    try:
        async with state.proxy() as data:
            journal_name = data['journal_name']
    except KeyError:
        print('Журнал не задан')

    try:
        async with state.proxy() as data:
            exception_list = data['exception_id_list']
    except KeyError:
        print('Эксепшн лист пустой')

    try:
        async with state.proxy() as data:
            author_name = data['author_name']
    except KeyError:
        print('Автор не задан')

    logging.info(f"{keywords=}")
    logging.info(f"{journal_name=}")
    logging.info(f"{exception_list=}")
    logging.info(f"{author_name=}")

    article_id = get_article_id(keywords, exception_list, journal_name, author_name)

    logging.info(f" Айдишники журналов {type(article_id)}")
    logging.info(f" Количество объектов {len(article_id)}")

    for i in article_id:
        info, url = get_article_info(i)
        logging.info(f"{info=}")
        logging.info(f"{url=}")
        await bot.send_message(chat_id=call.from_user.id,
                               text=info,
                               parse_mode=ParseMode.HTML,
                               reply_markup=url_and_gost_buttons(i, url))

    async with state.proxy() as data:
        if 'exception_id_list' in data:
            data['exception_id_list'] += ARTICLES_NUMBER
        else:
            data['exception_id_list'] = ARTICLES_NUMBER

    await bot.send_message(chat_id=call.from_user.id,
                           text='Продолжить поиск новых статей с заданными параметрами?',
                           reply_markup=agree_buttons(keywords))
    await state.reset_state(with_data=False)


@dp.message_handler(state='enter_journal')
async def articles_and_journal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        keywords = data['key']
        data['journal_name'] = message.text
    logging.info(f"Проверка, что сохранилось на этапе введения журнала {data['journal_name']}")

    await message.answer(text=f"Ключевые слова для поиска: {keywords} в журнале: {data['journal_name']}",
                         reply_markup=keywords_buttons(keywords))

    await state.reset_state(with_data=False)


@dp.callback_query_handler(journal_callback.filter())
async def set_journal_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        data['key'] = callback_data.get("keywords")
    # keywords = callback_data.get("keywords")
    logging.info(f"{data['key']}")
    await bot.send_message(chat_id=call.from_user.id, text="Введите название журнала", reply_markup=None)
    await state.set_state('enter_journal')


@dp.message_handler(state='enter_author')
async def articles_and_author(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        keywords = data['key']
        data['author_name'] = message.text
    logging.info(f"Проверка, что сохранилось на этапе введения журнала {data['author_name']}")

    await message.answer(text=f"Ключевые слова для поиска: {keywords} по имени автора: {data['author_name']}",
                         reply_markup=keywords_buttons(keywords))

    await state.reset_state(with_data=False)


@dp.callback_query_handler(author_callback.filter())
async def set_author_name(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        data['key'] = callback_data.get("keywords")
    # keywords = callback_data.get("keywords")
    logging.info(f"{data['key']}")
    await bot.send_message(chat_id=call.from_user.id, text="Введите имя автора", reply_markup=None)
    await state.set_state('enter_author')


@dp.callback_query_handler(gost_callback.filter())
async def get_gost_citation(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    citation = create_gost_link(callback_data.get("article_id"))
    await bot.send_message(chat_id=call.from_user.id, text=citation, reply_markup=None)
    # await bot.answer_inline_query(chat_id=call.from_user.id, text=citation, reply_markup=None)


@dp.callback_query_handler(cancel_callback.filter())
async def reset_proxy(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await bot.send_message(chat_id=call.from_user.id, text="Спасибо за обращение, надеемся было полезно ",
                           reply_markup=None)
    await state.reset_state()
